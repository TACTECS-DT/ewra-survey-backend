from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from ..validators import validate_file_type, validate_file_size
from ..custom_user import CustomUser
from django.shortcuts import get_object_or_404
import os 



            


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/',validators=[validate_file_type])
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    

        
    # Generic ForeignKey to handle multiple related models (e.g., Project, Task, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
    # to  save history referance record if deleted 
    # related_reference = models.TextField(blank=True, null=True)
    
        

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem if it exists
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        # Then delete the model instance
        super().delete(*args, **kwargs)
        
        
    # def re_link_to_new_record(self, new_instance):
    #     """
    #     Relink the attachment to a new model instance.
    #     """
    #     self.content_type = ContentType.objects.get_for_model(new_instance)
    #     self.object_id = new_instance.id
    #     # self.related_reference = f"Linked to {new_instance.__class__.__name__} #{new_instance.id}"
    #     self.save()
        
    def __str__(self):
        return self.file.name if self.file else 'No file'

    def file_exists(self):
        """Check if the file exists in the filesystem."""
        return self.file and default_storage.exists(self.file.name)


    def clean(self):
        """Manually run the validators on the file field."""
        file_field = self._meta.get_field('file')
        if self.file:
            for validator in file_field.validators:
                validator(self.file)

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validators run before saving
        super().save(*args, **kwargs)
        
        
        
    # ######################################
    # Example Usage
    # ######################################
    
    # 1. Creating an Attachment linked to a Project:
    #   project = Project.objects.get(id=1)
    #   attachment = Attachment.objects.create(
    #       file=my_uploaded_file,
    #       uploaded_by=request.user,  # optional, can be omitted
    #       content_type=ContentType.objects.get_for_model(Project),
    #       object_id=project.id,
    #       description="Sample description",  # optional, can be omitted
    #       related_reference="Project #1 details with name {project.name}",  # optional, can be omitted
    #   )
    
    # 2. Editing an Attachment (e.g., changing the linked model):
    #   attachment = Attachment.objects.get(id=1)
    #   task = Task.objects.get(id=5)
    #   attachment.content_type = ContentType.objects.get_for_model(Task)
    #   attachment.object_id = task.id
    #   attachment.file = new_file
    #   attachment.description = "Updated description"  # optional, can be omitted
    #   attachment.related_reference = "Updated Task  {task.id} with name {task.name}"  # optional, can be omitted
    #   attachment.save()
    
    # 3. Deleting a Project and updating attachments:
    #   project = Project.objects.get(id=1)
    #  
        # attachments = Attachment.objects.filter(
        # content_type=ContentType.objects.get_for_model(Project),
        # object_id=project.id
        #     )
        # for attachment in attachments:
        #     if not attachment.related_reference:  # If no related reference exists
        #         attachment.related_reference = f"Deleted Project #{project.id} with name {project.name}"
        #         attachment.save()
        
    #  project.delete()  # This will nullify content_type and object_id for related attachments
    
    # 4. Listing all Attachments for a specific Project:
    #   project = Project.objects.get(id=1)
    #   attachments = Attachment.objects.filter(
    #       content_type=ContentType.objects.get_for_model(Project),
    #       object_id=project.id
    #   )
    #   for attachment in attachments:
    #       print(attachment.file.name)
    #       print(attachment.description)  # Optional
    #       print(attachment.related_reference)  # Optional
    
    
    #  Re-link
    # attachment = Attachment.objects.get(id=1)

    # # Get the new instance to which you want to link the attachment (e.g., a new Project or Task)
    # new_project = Project.objects.get(id=2)  # For example, a new Project with ID 2

    # # Re-link the attachment to the new project
    # attachment.re_link_to_new_record(new_project)