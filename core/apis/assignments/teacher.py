from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint("teacher_assignments_resources", __name__)


@teacher_assignments_resources.route(
    "/assignments", methods=["GET"], strict_slashes=False
)
@decorators.auth_principal
def list_assignments(p):
    # """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
    # return {"message": "Teacher"}


@teacher_assignments_resources.route(
    "/assignments/grade", methods=["POST"], strict_slashes=False
)
@decorators.accept_payload
@decorators.auth_principal
def upsert_assignment(p, incoming_payload):
    """Updating the Grade"""
    # assignment = AssignmentSchema().load(incoming_payload) --- This will not work here.

    # I have to create a new Assignment Grade Schema

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Assignment.update_grade is my new method inside Assignment class
    graded_assignment = Assignment.update_grade(
        _id=grade_assignment_payload.id,
        new_grade=grade_assignment_payload.grade,
        principal=p,
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
