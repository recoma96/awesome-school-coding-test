const API_BASE_URL = "";  // Django Backend 서버와 동일한 도메인으로 본다
const ENROLLMENT_URL = `${API_BASE_URL}/api/course-enrollments`;

const FIELD_NAMES = ["name", "email", "address", "availableConnectionDate"];

const form = document.getElementById("enrollment-form");
const submitButton = document.getElementById("submit-button");
const formMessage = document.getElementById("form-message");

let isSubmitting = false;

/**
 * API 요청 직전에 사용하는 함수로
 * 서버에 요청하는 동안 버튼을 비활성화 하여 반복적으로 누르는 행태를 줄이는 것을
 * 목적으로 한다
 */
function setSubmitting(submitting) {
  isSubmitting = submitting;
  submitButton.disabled = submitting;
  submitButton.textContent = submitting ? "신청 중..." : "신청하기";
}

function showMessage(type, text) {
  formMessage.className = `form__message form__message--${type}`;
  formMessage.textContent = text;
  formMessage.hidden = false;
}

function setFieldError(fieldName, text) {
  const input = form.elements[fieldName];
  const errorElement = form.querySelector(`[data-error-for="${fieldName}"]`);
  errorElement.textContent = text;
  input.setAttribute("aria-invalid", text ? "true" : "false");
}

function clearErrors() {
  formMessage.hidden = true;
  formMessage.textContent = "";
  FIELD_NAMES.forEach((fieldName) => setFieldError(fieldName, ""));
}

// 브라우저 기본 검증(required, type=email, maxlength)을 필드 아래 메시지로 보여준다.
function validateClientSide() {
  let isValid = true;
  FIELD_NAMES.forEach((fieldName) => {
    const input = form.elements[fieldName];
    if (!input.checkValidity()) {
      setFieldError(fieldName, input.validationMessage);
      isValid = false;
    }
  });
  return isValid;
}

// DRF 400 응답: { "email": ["..."], "nonFieldErrors": ["..."] }
function showServerErrors(errors) {
  const formLevelMessages = [];

  Object.entries(errors).forEach(([key, messages]) => {
    const text = Array.isArray(messages) ? messages.join(" ") : String(messages);
    if (FIELD_NAMES.includes(key)) {
      setFieldError(key, text);
    } else { // ex: 이미 신청했는데 또 신청하려고 하는 경우s
      formLevelMessages.push(text);
    }
  });

  showMessage(
    "error",
    formLevelMessages.length > 0 ? formLevelMessages.join(" ") : "입력하신 내용을 다시 확인해주세요."
  );
}

/* 제출 버튼 핸들러 본문 */
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  // Enter 키 연타 등으로 중복 호출되는 것을 한 번 더 막는다.
  if (isSubmitting) {
    return;
  }

  clearErrors();
  if (!validateClientSide()) {
    return;
  }

  setSubmitting(true);
  let isCompleted = false;
  try { // 서버에 교육 신청을 요청하는 구간
    const payload = Object.fromEntries(
      FIELD_NAMES.map((fieldName) => [fieldName, form.elements[fieldName].value.trim()])
    );

    const response = await fetch(ENROLLMENT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.status === 201) {
      isCompleted = true;
      alert("신청이 완료되었습니다.");
      
      // 메인 페이지로 이동 
      // href 대신 replace를 사용해서 뒤로 갈 때 신청폼으로 가지 않게 처리
      window.location.replace("/");
      return;
    }

    if (response.status === 400) {
      showServerErrors(await response.json());
      return;
    }

    showMessage("error", "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
  } catch (error) {
    showMessage("error", "서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.");
  } finally {
    if (!isCompleted) { // 신청 완료시, alert 넘어가기 직전에 중복 클릭 방지
      setSubmitting(false);
    }
  }
});
