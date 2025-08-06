// Modal data for each department
const deptData = {
  cs: {
    title: "Department of Computer Science",
    vision: "To be a center of excellence in computer science, producing innovative and ethical technology leaders.",
    dean: "Welcome to the CS Department. We foster research, curiosity, and hands-on skills for the digital future.<br><b>- Dr. Anil Kumar, Dean</b>",
    activities: [
      "Annual AI Coding Marathon",
      "Student Research Symposium",
      "Robotics and IoT Workshops"
    ],
    faculty: [
      "Dr. Anil Kumar (Dean & Professor)",
      "Dr. Shreya Sen (AI & Data Science)",
      "Prof. Ravi Mohan (Software Engineering)"
    ],
    about: "Our Computer Science program emphasizes fundamentals, innovation, and application. Students undergo rigorous coursework in algorithms, programming, and domain electives with real-world projects.",
    downloads: [
      {name: "Eligibility Criteria (PDF)", link: "docs/cs_eligibility.pdf"},
      {name: "Fee Structure (PDF)", link: "docs/cs_fee.pdf"},
      {name: "Syllabus (PDF)", link: "docs/cs_syllabus.pdf"}
    ]
  },
  ba: {
    title: "Department of Business Administration",
    vision: "To nurture leaders for the global business environment with integrity and insight.",
    dean: "Join our Business Administration program for an immersive learning journey, combining theory and experiential projects.<br><b>- Dr. Pallavi Menon, Dean</b>",
    activities: [
      "Annual Entrepreneurship Summit",
      "Business Simulation Competitions",
      "Industrial Visits & Guest Lectures"
    ],
    faculty: [
      "Dr. Pallavi Menon (Dean)",
      "Prof. Arjun Rajan (Finance)",
      "Dr. Sheila D’Souza (Marketing Management)"
    ],
    about: "Our BBA and MBA programs blend core business concepts with contemporary practices, internships, and leadership development labs.",
    downloads: [
      {name: "Eligibility Criteria (PDF)", link: "docs/ba_eligibility.pdf"},
      {name: "Fee Structure (PDF)", link: "docs/ba_fee.pdf"},
      {name: "Syllabus (PDF)", link: "docs/ba_syllabus.pdf"}
    ]
  },
  bio: {
    title: "Department of Biosciences",
    vision: "To advance knowledge in life sciences for societal and environmental benefit.",
    dean: "Our department combines research in biotechnology with hands-on lab training, preparing students for research and industry.<br><b>- Dr. Maya Ghosh, Dean</b>",
    activities: [
      "Biotech Hackathon",
      "Nature Study Camps",
      "Guest Seminars by Eminent Scientists"
    ],
    faculty: [
      "Dr. Maya Ghosh (Dean)",
      "Dr. Suneel Varma (Biotechnology)",
      "Dr. Priya Nair (Environmental Sciences)"
    ],
    about: "We offer undergraduate and postgraduate programs in biosciences, focusing on research skills and sustainable solutions.",
    downloads: [
      {name: "Eligibility Criteria (PDF)", link: "docs/bio_eligibility.pdf"},
      {name: "Fee Structure (PDF)", link: "docs/bio_fee.pdf"},
      {name: "Syllabus (PDF)", link: "docs/bio_syllabus.pdf"}
    ]
  }
};

document.querySelectorAll('.department-card').forEach((card) => {
  card.addEventListener('click', function () {
    const dept = card.getAttribute('data-dept');
    const data = deptData[dept];
    if (!data) return;
    // Fill modal info
    document.getElementById('modalDeptTitle').innerHTML = data.title;
    document.getElementById('modalDeptVision').textContent = data.vision;
    document.getElementById('modalDeptDean').innerHTML = data.dean;
    // Activities
    let acts = '';
    data.activities.forEach(a => acts += `<li>${a}</li>`);
    document.getElementById('modalDeptActivities').innerHTML = acts;
    // Faculty
    let facs = '';
    data.faculty.forEach(f => facs += `<li>${f}</li>`);
    document.getElementById('modalDeptFaculty').innerHTML = facs;
    document.getElementById('modalDeptAbout').textContent = data.about;
    // Downloads
    let dl = '';
    data.downloads.forEach(d => dl += `<li><a href="${d.link}" target="_blank"><b>${d.name}</b></a></li>`);
    document.getElementById('modalDeptDownloads').innerHTML = dl;

    document.getElementById('deptModal').style.display = 'block';
  });
});

document.getElementById('deptModalClose').onclick = function() {
  document.getElementById('deptModal').style.display = 'none';
};
window.onclick = function(event) {
  const modal = document.getElementById('deptModal');
  if (event.target == modal) modal.style.display = "none";
};
