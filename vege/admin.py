from django.contrib import admin
from django.db.models import Sum
# Register your models here.
from .models import *
admin.site.register(Receipe)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Subject)
class SubjectMarksAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks']
    def __str__(self) -> str:
        return self.subject_name
admin.site.register(SubjectMarks,SubjectMarksAdmin)
class ReportCardAdmin(admin.ModelAdmin):
    list_display=['student','student_rank','total_marks','date_of_report']
    #ordering=['-rank']
    def total_marks(self,obj):
        subject_marks=SubjectMarks.objects.filter(student=obj.student)
        marks=subject_marks.aggregate(marks=Sum('marks'))
        return marks['marks']
admin.site.register(ReportCard,ReportCardAdmin)

