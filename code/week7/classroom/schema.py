import graphene
from graphene_django.types import DjangoObjectType
from .models import Student

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("id", "name", "email")

# MUTATIONS
class CreateStudent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    student = graphene.Field(StudentType)

    def mutate(root, info, name, email):
        student = Student(name=name, email=email)
        student.save()
        return CreateStudent(student=student)

class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.String()

    student = graphene.Field(StudentType)

    def mutate(root, info, id, name=None, email=None):
        student = Student.objects.get(pk=id)
        if name:
            student.name = name
        if email:
            student.email = email
        student.save()
        return UpdateStudent(student=student)

class DeleteStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    def mutate(root, info, id):
        student = Student.objects.get(pk=id)
        student.delete()
        return DeleteStudent(ok=True)

# Combine queries and mutations
class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    student_by_id = graphene.Field(StudentType, id=graphene.Int(required=True))

    def resolve_all_students(root, info):
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        return Student.objects.get(pk=id)

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
