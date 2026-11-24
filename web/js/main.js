const landingData = {
  title: "챗GPT 히어로",
  introduction: "버추얼 코치와의 1:1 학습으로 생성형 AI 활용법과 윤리를 익히고,\n학업과 생활 속 문제를 창의적으로 해결해보는 실전형 디지털 리터러시 교육",
  curriculums: [
    {
      "order": 1,
      "topic": "챗GPT 완전정복!",
      "activity": "생성형AI의 개념 이해",
      "content": "챗GPT의 기본 원리를 배우고 실습하며 인공지능으로 변화할 미래 사회의 모습을 생각해봅니다.",
      "imgSrc": "/assets/curriculum-1.jpg",
    },
    {
      "order": 2,
      "topic": "GPT 200% 활용법",
      "activity": "프롬포트 생성팁과 AI 활용시 주의사항 이해",
      "content": "양질의 정보를 얻기 위한 효과적 질문 방법을 배우고 AI 활용시 정보 이용 윤리 및 주의사항을 익힙니다.",
      "imgSrc": "/assets/curriculum-2.jpg",
    },
    {
      "order": 3,
      "topic": "10대를 위한 챗GPT",
      "activity": "AI 활용 능력 및 문제해결 역량 향상",
      "content": "AI를 도구삼아 학업 및 학교 생활에서 생산성을 향상시킬 수 있는 방법과 문제 해결 과정을 배웁니다.",
      "imgSrc": "/assets/curriculum-3.jpg",
    }
  ]
}

const title = document.getElementById("title");
const introduction = document.getElementById("introduction");

title.textContent = landingData.title;
introduction.textContent = landingData.introduction;

const curriculumList = document.getElementById("curriculum-list");
const cardTemplate = document.getElementById("curriculum-card-template");
const cards = landingData.curriculums
  .sort((a, b) => a.order - b.order)
  .map((curriculum) => {
    const card = cardTemplate.content.firstElementChild.cloneNode(true);

    const image = card.querySelector(".curriculum-card__image");
    image.src = curriculum.imgSrc;
    image.alt = curriculum.topic;

    card.querySelector(".curriculum-card__order").textContent = `${curriculum.order}회차`;
    card.querySelector(".curriculum-card__topic").textContent = curriculum.topic;
    card.querySelector(".curriculum-card__activity").textContent = curriculum.activity;
    card.querySelector(".curriculum-card__content").textContent = curriculum.content;
    return card;
  });

curriculumList.replaceChildren(...cards);