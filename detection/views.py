from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

from .models import Patient, GlaucomaTest
from .forms import PatientForm, GlaucomaTestForm, PatientLookupForm
from .utils import predict_glaucoma, generate_result_visualization

def home(request):
    """Home page with the form to upload an image for analysis."""
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        test_form = GlaucomaTestForm(request.POST, request.FILES)
        
        if patient_form.is_valid() and test_form.is_valid():
            try:
                with transaction.atomic():
                    # Get or create patient
                    email = patient_form.cleaned_data['email']
                    patient, created = Patient.objects.get_or_create(
                        email=email,
                        defaults={'name': patient_form.cleaned_data['name']}
                    )
                    
                    # If patient exists but with different name, update the name
                    if not created and patient.name != patient_form.cleaned_data['name']:
                        patient.name = patient_form.cleaned_data['name']
                        patient.save()
                    
                    # Create test record
                    test = test_form.save(commit=False)
                    test.patient = patient
                    test.save()
                
                # Redirect to processing view
                return redirect('process_test', test_id=test.id)
            
            except Exception as e:
                messages.error(request, f"Error processing your request: {str(e)}")
    else:
        patient_form = PatientForm()
        test_form = GlaucomaTestForm()
    
    return render(request, 'detection/home.html', {
        'patient_form': patient_form,
        'test_form': test_form,
    })

def process_test(request, test_id):
    """Process the uploaded image and show results."""
    test = get_object_or_404(GlaucomaTest, id=test_id)
    
    # Only process if status is pending
    if test.status == 'pending':
        test.mark_processing()
        
        try:
            # Make prediction
            result = predict_glaucoma(test.image.path)
            
            # Generate visualization image
            result_image_io = generate_result_visualization(test.image.path, result)
            
            # Save result image
            image_name = f"result_{test.id}.png"
            test.result_image.save(image_name, ContentFile(result_image_io.getvalue()), save=False)
            
            # Update test with results
            test.mark_completed(
                is_glaucoma=result['is_glaucoma'],
                raw_score=result['raw_score'],
                confidence_score=result['confidence']
            )
            
        except Exception as e:
            test.mark_failed(str(e))
            messages.error(request, f"Error processing image: {str(e)}")
    
    return render(request, 'detection/result.html', {
        'test': test
    })

def records(request):
    """Page to view patient's past records."""
    tests = []
    patient = None
    
    if request.method == 'POST':
        form = PatientLookupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                patient = Patient.objects.get(email=email)
                tests = GlaucomaTest.objects.filter(patient=patient)
                
                if not tests:
                    messages.info(request, "No test records found for this email.")
            except Patient.DoesNotExist:
                messages.warning(request, "No patient found with this email address.")
                
    else:
        form = PatientLookupForm()
    
    return render(request, 'detection/records.html', {
        'form': form,
        'tests': tests,
        'patient': patient
    })

def test_detail(request, test_id):
    """View a specific test result."""
    test = get_object_or_404(GlaucomaTest, id=test_id)
    return render(request, 'detection/test_detail.html', {
        'test': test
    })

@require_POST
def cancel_test(request, test_id):
    """Cancel a pending test."""
    test = get_object_or_404(GlaucomaTest, id=test_id)
    
    if test.status == 'pending' or test.status == 'processing':
        test.mark_failed("Test cancelled by user")
        messages.success(request, "Test has been cancelled.")
    else:
        messages.error(request, "Cannot cancel a test that is already completed or failed.")
    
    return redirect('records')