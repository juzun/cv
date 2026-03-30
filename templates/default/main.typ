#import "components.typ": *

#let data = json("content.json")
#let meta = data.meta
#let sections = data.sections

// Page setup
#set page(
  paper: "a4",
  margin: (top: 1.8cm, bottom: 1.8cm, left: 2cm, right: 2cm),
  numbering: none,
)

#set text(
  font: "Ubuntu",
  size: 9.5pt,
  fill: rgb("#1a1a1a"),
  lang: "en",
)

#set par(justify: true, leading: 0.72em, spacing: 0.9em)

#show link: it => text(fill: rgb("#1a1a1a"), it)

// Header
#align(center)[
  #text(upper(meta.name), weight: "bold", size: 20pt, tracking: 4pt)
  #v(5pt)
  #text(meta.title, size: 10.5pt, fill: rgb("#444444"))
  #v(8pt)
  #contact-bar(meta.contact)
]

#v(8pt)
#line(length: 100%, stroke: 1.2pt + rgb("#2a2a2a"))

// Sections
#for section in sections {
  if section.type == "summary" {
    section-header("Professional Summary")
    summary-block(section.content)
  } else if section.type == "experience" {
    section-header("Experience")
    for company in section.content {
      experience-entry(
        company.company,
        company.roles,
        location: if "location" in company { company.location } else { none },
      )
    }
  } else if section.type == "education" {
    section-header("Education")
    for entry in section.content {
      education-entry(entry)
    }
  } else if section.type == "skills" {
    section-header("Skills")
    for cat in section.content {
      skill-category(cat)
    }
  } else if section.type == "certifications" {
    section-header("Certifications")
    certification-list(section.content)
  } else if section.type == "languages" {
    section-header("Languages")
    for lang in section.content {
      language-entry(lang)
    }
  } else if section.type == "hobbies" {
    section-header("Interests")
    hobbies-block(section.content)
  }
}
