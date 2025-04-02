from django import forms
from .models import Patient, GlaucomaTest

class PatientForm(forms.ModelForm):
    """Form for patient information."""
    class Meta:
        model = Patient
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

class GlaucomaTestForm(forms.ModelForm):
    """Form for uploading fundus images."""
    class Meta:
        model = GlaucomaTest
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_image(self):
        """Validate the uploaded image."""
        image = self.cleaned_data.get('image')
        
        # Check if an image was uploaded
        if not image:
            raise forms.ValidationError("No image selected.")
        
        # Check file extension
        allowed_extensions = ['jpg', 'jpeg', 'png']
        ext = image.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise forms.ValidationError(f"Unsupported file format. Please use: {', '.join(allowed_extensions)}")
        
        # Check file size (limit to 5MB)
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image file too large. Maximum size is 5MB.")
        
        return image

class PatientLookupForm(forms.Form):
    """Form for looking up a patient by email."""
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email to view past records'})
    )