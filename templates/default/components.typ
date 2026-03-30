// Spacing constants
#let SECTION-SPACE-ABOVE  = 12pt   // vertical gap BEFORE each section header
#let SECTION-SPACE-BELOW  = 6pt    // vertical gap AFTER the section rule
#let SECTION-RULE-WEIGHT  = 0.6pt  // thickness of section separator line
#let COMPANY-SPACE-ABOVE  = 8pt    // gap between companies in experience
#let ROLE-SPACE-ABOVE     = 4pt    // gap between roles within one company
#let BULLET-INDENT        = 10pt   // left indent for bullet text
#let BULLET-SPACE-BETWEEN = 6pt    // vertical gap between bullets
#let ENTRY-SPACE-BELOW    = 6pt    // gap after education / cert / lang entries
#let BODY-SIZE            = 9.5pt  // base font size for body text
#let SMALL-SIZE           = 8.5pt  // secondary / muted text size
#let HEADER-SIZE          = 10pt   // section header font size
#let DATE-WIDTH           = 105pt  // fixed column width for right-aligned dates

// Colours
#let CLR-BODY  = rgb("#1a1a1a")
#let CLR-MUTED = rgb("#555555")
#let CLR-RULE  = rgb("#3a3a3a")

// Section header
#let section-header(title) = {
  v(SECTION-SPACE-ABOVE)
  text(upper(title), weight: "bold", size: HEADER-SIZE, tracking: 1.5pt, fill: CLR-BODY)
  v(3pt)
  line(length: 100%, stroke: SECTION-RULE-WEIGHT + CLR-RULE)
  v(SECTION-SPACE-BELOW)
}

// Contact bar
#let contact-bar(contact) = {
  set text(size: SMALL-SIZE, fill: CLR-MUTED)
  let items = ()
  if "email" in contact { items.push(contact.email) }
  if "phone" in contact { items.push(contact.phone) }
  if "location" in contact { items.push(contact.location) }
  if "github" in contact {
    items.push(link(contact.github)[GitHub])
  }
  if "linkedin" in contact {
    items.push(link(contact.linkedin)[LinkedIn])
  }
  align(center, items.join[ #h(8pt) | #h(8pt) ])
}

// Summary
#let summary-block(content) = {
  set text(size: BODY-SIZE)
  set par(justify: true, leading: 0.75em)
  content
}

// Experience
#let experience-entry(company, roles, location: none) = {
  v(COMPANY-SPACE-ABOVE)

  // Company header row — bold name, optional location
  {
    let t = text(company, weight: "bold", size: BODY-SIZE)
    if location != none {
      t = t + text(", " + location, size: SMALL-SIZE, fill: CLR-MUTED)
    }
    t
  }

  for role in roles {
    v(ROLE-SPACE-ABOVE)

    // Title | Department
    grid(
      columns: (1fr, DATE-WIDTH),
      column-gutter: 8pt,
      {
        text(role.title, style: "italic", size: BODY-SIZE)
        if "department" in role and role.department != "" {
          text(" — " + role.department, size: SMALL-SIZE, fill: CLR-MUTED)
        }
      },
      align(right, text(
        if "end" in role { role.start + " - " + str(role.end) } else { str(role.start) },
        size: SMALL-SIZE, fill: CLR-MUTED)),
    )

    v(3pt)

    // Bullet list
    set text(size: BODY-SIZE)
    set par(justify: true, leading: 0.72em)
    for bullet in role.bullets {
      block(
        inset: (left: BULLET-INDENT),
        above: BULLET-SPACE-BETWEEN,
        below: BULLET-SPACE-BETWEEN,
      )[#text("–", fill: CLR-MUTED) #h(5pt) #bullet]
    }
  }
}

// Education
#let education-entry(entry) = {
  grid(
    columns: (1fr, DATE-WIDTH),
    column-gutter: 8pt,
    {
      text(entry.degree, weight: "bold", size: BODY-SIZE)
      linebreak()
      text(entry.institution, size: BODY-SIZE)
      if "location" in entry {
        text(", " + entry.location, size: SMALL-SIZE, fill: CLR-MUTED)
      }
      if "details" in entry and entry.details != "" {
        linebreak()
        text(entry.details, size: SMALL-SIZE, fill: CLR-MUTED)
      }
    },
    align(right, text(
      if "end" in entry { entry.start + " - " + str(entry.end) } else { str(entry.start) },
      size: SMALL-SIZE, fill: CLR-MUTED)),
  )
  v(ENTRY-SPACE-BELOW)
}

// Skills
#let skill-category(cat) = {
  set text(size: BODY-SIZE)

  // Category + first group on one line using a grid
  grid(
    columns: (auto, 1fr),
    column-gutter: 8pt,
    text(cat.category, weight: "bold"),
    {
      for (i, item) in cat.items.enumerate() {
        if i > 0 { v(1pt) }
        if item.group != "" {
          text(item.group + ": ", size: SMALL-SIZE, fill: CLR-MUTED)
        }
        text(item.entries.join(" · "), size: BODY-SIZE)
        if i < cat.items.len() - 1 { linebreak() }
      }
    },
  )
  v(5pt)
}

// Certifications
#let certification-list(certs) = {
  set text(size: BODY-SIZE)
  for cert in certs {
    block(
      inset: (left: BULLET-INDENT),
      above: 3pt,
      below: 3pt,
    )[#text("-", fill: CLR-MUTED) #h(5pt) #cert]
  }
}

// Languages
#let language-entry(lang) = {
  set text(size: BODY-SIZE)
  let filled = lang.level
  let empty = 10 - lang.level
  grid(
    columns: (60pt, auto),
    column-gutter: 8pt,
    text(lang.name, weight: "bold"),
    text(
      "●" * filled + "○" * empty,
      size: 7.5pt,
      fill: CLR-MUTED,
      baseline: -1pt,
    ),
  )
  v(2pt)
}

// Hobbies
#let hobbies-block(content) = {
  set text(size: BODY-SIZE)
  set par(justify: true, leading: 0.72em)
  content
}
