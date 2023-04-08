def test_get_assignments_student_1(client, h_student_1):
    response = client.get("/student/assignments", headers=h_student_1)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["student_id"] == 1


def test_get_assignments_student_unauthorized(client):
    response = client.get("/student/assignments")
    assert response.status_code == 401


def test_get_assignments_student_2(client, h_student_2):
    response = client.get("/student/assignments", headers=h_student_2)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["student_id"] == 2


def test_post_assignment_student_1(client, h_student_1):
    content = "ABCD TESTPOST"

    response = client.post(
        "/student/assignments", headers=h_student_1, json={"content": content}
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["content"] == content
    assert data["state"] == "DRAFT"
    assert data["teacher_id"] is None


def test_post_assignments_student_unauthorized(client):
    response = client.post(
        "/student/assignments", json={"content": "test unauthorized post"}
    )
    assert response.status_code == 401


def test_post_assignment_student_1_without_content(client, h_student_1):
    response = client.post("/student/assignments", headers=h_student_1)

    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "ValidationError"
    assert error_response["message"] == {"_schema": ["Invalid input type."]}


def test_post_assignment_student_2(client, h_student_2):
    content = "ABCD TESTPOST"

    response = client.post(
        "/student/assignments", headers=h_student_2, json={"content": content}
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["content"] == content
    assert data["state"] == "DRAFT"
    assert data["teacher_id"] is None


def test_post_assignment_student_2_without_content(client, h_student_2):
    response = client.post("/student/assignments", headers=h_student_2)

    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "ValidationError"
    assert error_response["message"] == {"_schema": ["Invalid input type."]}


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": 2, "teacher_id": 2},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["student_id"] == 1
    assert data["state"] == "SUBMITTED"
    assert data["teacher_id"] == 2


def test_submit_invalid_assignment_student_1(client, h_student_1):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": 2000, "teacher_id": 2},
    )

    error_response = response.json
    assert response.status_code == 404
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "No assignment with this id was found"


def submitted_to_wrong_student_error(client, h_student_2):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_2,
        json={"id": 2, "teacher_id": 2},
    )
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "No assignment with this id was found"


def test_submit_assignment_student_2(client, h_student_2):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_2,
        json={"id": 7, "teacher_id": 2},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["student_id"] == 2
    assert data["state"] == "SUBMITTED"
    assert data["teacher_id"] == 2


def test_submit_invalid_assignment_student_2(client, h_student_2):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_2,
        json={"id": 2000, "teacher_id": 2},
    )

    error_response = response.json
    assert response.status_code == 404
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "No assignment with this id was found"


def test_assingment_resubmitt_error_for_student_1(client, h_student_1):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": 2, "teacher_id": 2},
    )
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "This assignment is already Submitted"


def test_assingment_resubmitt_error_for_student_2(client, h_student_2):
    response = client.post(
        "/student/assignments/submit",
        headers=h_student_2,
        json={"id": 3, "teacher_id": 2},
    )
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "This assignment is already Submitted"
