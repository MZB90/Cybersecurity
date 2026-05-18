
# Stanford CoreNLP - CV Parsing Web Integration for Ajirika HCM

> **Type:** Technical Evaluation and Integration Report - Internship Portfolio
> **Domain:** Natural Language Processing / Java Web Development / HCM Systems
> **Status:** Complete
> **Date:** 2026-05-15
> **Authors:** Samuel Dabaly & Upao Mazibo
> **Repository:** https://github.com/OpenBaraza/ajirika
> **Live Interface:** https://ajirika.hcm.co.ke/

---

## Table of Contents

- [[#Objective]]
- [[#Why Stanford CoreNLP Was Explored]]
- [[#Phase 1 - Repository Analysis]]
- [[#Phase 1 - Compatibility Findings]]
- [[#Phase 1 - Architecture Decision]]
- [[#Phase 2 - Standalone POC Implementation]]
- [[#Phase 2 - Web Integration Implementation]]
- [[#Testing Process and Results]]
- [[#NLP Quality Evaluation]]
- [[#Challenges Encountered]]
- [[#Lessons Learned]]
- [[#Future Recommendations for Ajirika]]

---

## Objective 

This project documents a two-phase evaluation of Stanford CoreNLP as a potential NLP engine for the Ajirika HCM platform. The evaluation was structured as follows:

Phase 1 involved a standalone proof of concept to answer one specific question: can Stanford CoreNLP meaningfully process a CV-sized document rather than a few test sentences? This phase used a separate Maven project independent of the Ajirika codebase.

Phase 2 involved integrating Stanford CoreNLP directly into the running Ajirika web application, replacing the personal information extraction logic in the existing NLP pipeline, and verifying end-to-end operation through the browser interface.

This was a feasibility evaluation, not a production implementation.

---

## Why Stanford CoreNLP Was Explored

Ajirika is a Human Capital Management platform built around the concept of a standardised, machine-readable CV format. A natural capability for such a platform is automated CV parsing - extracting structured information from unstructured candidate documents.

The existing codebase had already declared Apache OpenNLP as its NLP library. However, the OpenNLP implementation required seven custom trained model files (en-ner-person.bin, en-ner-organization.bin, en-ner-cv.bin, cust-person.bin, en-ner-education.bin, en-ner-experience.bin, en-sent.bin) that were absent from the repository. The OpenNLP pipeline was therefore non-functional without significant additional work to train and supply those models.

Stanford CoreNLP was evaluated as an alternative because:

- It is Java-native, matching Ajirika's backend language exactly
- It ships pre-trained English NER models requiring no custom training to run
- It is open-source with no API costs or rate limits
- It runs entirely on-premise with no external data transmission
- A local proof of concept had already been completed validating the environment

---

## Phase 1 - Repository Analysis

### Source

Repository: OpenBaraza/ajirika on GitHub
Live interface: https://ajirika.hcm.co.ke/

### Project Nature

Ajirika is an early-stage open-source initiative started in October 2025, aiming to establish a standardised JSON-based CV format for Kenyan and broader African job markets. It is not a fork of the Baraza XML framework as initially assumed from the organisation profile. It is a fresh Maven WAR project built on standard Jakarta Servlet technology.

### Confirmed Technology Stack

| Layer | Technology |
|---|---|
| Backend | Java |
| Build System | Apache Maven 3.x |
| Web Runtime | Apache Tomcat 10.1 |
| Database | PostgreSQL 18 |
| Frontend | JSP with Tailwind CSS |
| NLP Library (declared) | Apache OpenNLP 2.5.2 |
| Document Parsing (declared) | Apache Tika 3.1.0 |
| Data Format | JSON via org.json |

### Existing CV Processing Architecture

The repository contained a complete, well-structured CV processing pipeline at the time of analysis:

- `readCV.java` - uses Tika with Jsoup to extract and structure text from uploaded PDF, DOC, and DOCX files
- `breakdownCV.java` - rule-based section detection and parsing for education, experience, skills, and references, with an OpenNLP sentence model fallback
- `uploadProcess.java` - Jakarta servlet mapped to /processCV, handling file upload, pipeline orchestration, log capture, and JSON response
- `processCV.jsp` - a fully built frontend with file upload form, processing log tab, and structured results tab displaying name, email, phone, education, experience, skills, and referees

The frontend JavaScript in processUpload.js was already wired to POST to the /processCV endpoint and render a specific JSON response shape. The backend servlet and the frontend were therefore already coordinated. The only missing piece was a functional NLP engine.

### Key Structural Finding

The section detection in breakdownCV.java falls back to line-by-line parsing when the OpenNLP sentence model is absent. This means the pipeline runs without OpenNLP models, though with reduced accuracy. The analyzeCV.java class, which loads all the missing OpenNLP model files, is entirely unused by the main pipeline.

---

## Phase 1 - Compatibility Findings

### Language Compatibility

Both Ajirika and Stanford CoreNLP are Java. No bridging, wrapping, or language interop is required. Compatibility at the language level is complete.

### Build System Compatibility

Ajirika uses Maven. Stanford CoreNLP is distributed via Maven Central. Adding CoreNLP to the project required two dependency declarations in pom.xml and a compiler target change from Java 8 to Java 11, since CoreNLP 4.5.x requires a minimum of Java 11.

### Memory Requirements

Stanford CoreNLP loads approximately 400MB of pre-trained English model data into JVM heap on startup. The pipeline object must be initialised once and reused across requests. Tomcat must be started with -Xmx4g or equivalent. Without this, the servlet will throw OutOfMemoryError during initialisation.

### NER Accuracy Assessment (from standalone POC)

Testing against a real 303-word cybersecurity CV produced the following findings:

Reliable extractions:
- Email addresses: perfect accuracy, both addresses captured
- Dates and date ranges: excellent, all six dates correctly identified
- Cities: correct, Nairobi and Kinshasa both detected
- Countries: correct, including multi-token span "Democratic Republic of the Congo"
- Western organisation names: good, Google, Catholic University of Eastern Africa, Tata Group

Unreliable extractions:
- Candidate name: missed entirely - "UPAO MAZIBO" tagged as O (outside), a known limitation with African names not present in the training corpus
- Security tools: Wireshark, Nmap, Tcpdump misclassified as LOCATION or PERSON
- Deloitte, Mastercard: missed due to fragmented CV sentence structure
- African languages: Swahili and Lingala not recognised as LANGUAGE entities
- Skills and certifications: no corresponding entity types exist in CoreNLP's default label set

### Integration Risk Assessment

| Dimension | Assessment |
|---|---|
| Language compatibility | Full - both Java |
| Build integration | Low risk - Maven dependency |
| Memory management | Medium risk - requires explicit heap configuration |
| NER accuracy on African CVs | High risk - name recognition fails on African names |
| NER accuracy on structured fields | Low risk - dates, emails, cities reliable |
| Section parsing of CV structure | Medium risk - CV formatting breaks sentence boundary detection |

---

## Phase 1 - Architecture Decision

### Decision: Standalone CLI First, Then Web Integration

For the standalone POC, the decision was to build an executable fat JAR that accepts a CV file path as a command-line argument, extracts text, runs the CoreNLP pipeline, and prints annotated output to the console. This approach:

- Isolated NLP behaviour from the Ajirika codebase entirely
- Reused the existing corenlp-demo Maven project
- Introduced only one new dependency - Apache PDFBox 3.0.3 for PDF extraction
- Produced directly evaluable output with minimal debugging surface
- Was trivially removable if the evaluation concluded negatively

### Decision: Surgical Integration for Web Phase

For web integration, the decision was to not create a new servlet but to modify the existing breakdownCV.java to replace its personal information extraction logic with CoreNLP NER while leaving all rule-based section detection and parsing intact. This was the lowest-risk integration path because:

- The URL mapping, file handling, log capture, and JSON response format remained unchanged
- The existing frontend required no modification
- Only the extractPersonalInfo method was replaced
- The change was localised to a single method in a single file

---

## Phase 2 - Standalone POC Implementation

### Environment

| Component | Details |
|---|---|
| Machine | Lenovo ThinkPad |
| OS | Kali Linux (6.19.14+kali-amd64) |
| RAM | 16GB |
| IDE | VSCodium |
| Build Tool | Apache Maven 3.9.12 |
| Java Version | OpenJDK 25.0.3-ea |
| CoreNLP Version | 4.5.10 |
| PDFBox Version | 3.0.3 |

### Dependencies Added to corenlp-demo/pom.xml

```xml
<dependency>
  <groupId>edu.stanford.nlp</groupId>
  <artifactId>stanford-corenlp</artifactId>
  <version>4.5.10</version>
</dependency>

<dependency>
  <groupId>edu.stanford.nlp</groupId>
  <artifactId>stanford-corenlp</artifactId>
  <version>4.5.10</version>
  <classifier>models</classifier>
</dependency>

<dependency>
  <groupId>org.apache.pdfbox</groupId>
  <artifactId>pdfbox</artifactId>
  <version>3.0.3</version>
</dependency>
```

### Implementation

The final App.java accepted a file path argument, extracted text using PDFBox (for PDF) or Files.readString (for TXT), annotated the full document through CoreNLP's tokenize, ssplit, pos, lemma, ner pipeline, and produced two output sections: a named entity summary grouped by type, and a full per-sentence token-level annotation table.

Run command:

```bash
java -Xmx4g -jar target/corenlp-demo-1.0-SNAPSHOT.jar /path/to/cv.pdf
```

### Standalone Test Results

The pipeline processed 303 words across 16 detected sentences from a real PDF CV with no errors. Model loading completed in approximately 12 seconds. Output was complete and readable. The feasibility question was answered affirmatively: CoreNLP can process a CV-sized document.

---

## Phase 2 - Web Integration Implementation

### Prerequisites Configured

**Database:** The baraza PostgreSQL database existed on the system. Schema was loaded via the project's SQL migration files:

```bash
sudo -u postgres psql -d baraza -f db/01.baraza.sql
sudo -u postgres psql -d baraza -f db/02.profile.sql
```

**JNDI Datasource:** Configured in /opt/tomcat/conf/context.xml:

```xml
<Resource name="jdbc/database"
          auth="Container"
          type="javax.sql.DataSource"
          driverClassName="org.postgresql.Driver"
          url="jdbc:postgresql://localhost:5432/baraza"
          username="postgres"
          password="postgres"
          maxTotal="20"
          maxIdle="10"
          maxWaitMillis="-1"/>
```

The PostgreSQL JDBC driver JAR was copied from the local Maven cache into /opt/tomcat/lib/ to make it available at the Tomcat server level.

### Dependencies Added to Ajirika pom.xml

```xml
<dependency>
  <groupId>edu.stanford.nlp</groupId>
  <artifactId>stanford-corenlp</artifactId>
  <version>4.5.10</version>
</dependency>

<dependency>
  <groupId>edu.stanford.nlp</groupId>
  <artifactId>stanford-corenlp</artifactId>
  <version>4.5.10</version>
  <classifier>models</classifier>
</dependency>
```

The compiler target was updated from Java 8 to Java 11 to satisfy CoreNLP's minimum requirement.

### Defensive Changes to uploadProcess.java

Two null-safety fixes were applied to prevent NullPointerExceptions when the database connection is unavailable or when no authenticated user is present during testing:

```java
// Before
if (!db.isValid()) db.reconnect("java:/comp/env/jdbc/database");

// After
if (db != null && !db.isValid()) db.reconnect("java:/comp/env/jdbc/database");
```

```java
// Before
userID = getLoggedInUserId(request);

// After
try {
    userID = getLoggedInUserId(request);
} catch (Exception e) {
    System.out.println("No authenticated user, defaulting userID to -1");
    userID = "-1";
}
```

### CoreNLP Integration in breakdownCV.java

The extractPersonalInfo method was replaced entirely. The new implementation:

1. Builds a CoreNLP pipeline with tokenize, ssplit, pos, lemma, ner annotators
2. Annotates the full extracted CV text
3. Logs all detected entity mentions for evaluation visibility
4. Assigns the first PERSON entity as the candidate name
5. Assigns the first EMAIL entity as the email address
6. Falls back to regex for email if CoreNLP missed it
7. Falls back to the first line of the CV text if CoreNLP missed the name
8. Uses regex for phone number extraction regardless, as CoreNLP does not produce a PHONE entity type
9. Continues with the existing labeled field extraction for address and supplementary fields

```java
private void extractPersonalInfo(String plainText, JSONObject result) {
    JSONObject personalInfo = new JSONObject();

    try {
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner");
        StanfordCoreNLP nlpPipeline = new StanfordCoreNLP(props);
        CoreDocument doc = new CoreDocument(plainText);
        nlpPipeline.annotate(doc);

        System.out.println("[CoreNLP] Entity mentions detected:");
        for (CoreEntityMention em : doc.entityMentions()) {
            System.out.println("  " + em.entityType() + ": " + em.text());

            if (em.entityType().equals("PERSON") && !personalInfo.has("name")) {
                personalInfo.put("name", em.text());
                System.out.println("[CoreNLP] Assigned name: " + em.text());
            }
            if (em.entityType().equals("EMAIL") && !personalInfo.has("email")) {
                personalInfo.put("email", em.text());
                System.out.println("[CoreNLP] Assigned email: " + em.text());
            }
        }
    } catch (Exception e) {
        System.out.println("[CoreNLP] Pipeline failed, falling back to regex: " + e.getMessage());
    }

    // Regex fallback for email
    if (!personalInfo.has("email")) {
        Matcher emailMatcher = EMAIL_PATTERN.matcher(plainText);
        if (emailMatcher.find()) {
            personalInfo.put("email", emailMatcher.group(0));
        }
    }

    // First-line fallback for name
    if (!personalInfo.has("name")) {
        String firstLine = plainText.trim().split("\\n")[0].trim();
        if (firstLine.length() > 2 && firstLine.length() < 60) {
            personalInfo.put("name", firstLine);
        }
    }

    // Regex for phone
    Matcher phoneMatcher = PHONE_PATTERN.matcher(plainText);
    if (phoneMatcher.find()) {
        personalInfo.put("phone", phoneMatcher.group(0));
    }

    // Labeled field extraction
    Matcher personalInfoMatcher = PERSONAL_INFO_PATTERN.matcher(plainText);
    while (personalInfoMatcher.find()) {
        String infoLine = personalInfoMatcher.group(0).toLowerCase();
        String value = personalInfoMatcher.group(1).trim();
        if (infoLine.contains("address") && !personalInfo.has("address"))
            personalInfo.put("address", value);
        else if (infoLine.contains("name") && !personalInfo.has("name"))
            personalInfo.put("name", value);
        else if ((infoLine.contains("phone") || infoLine.contains("mobile"))
                && !personalInfo.has("phone"))
            personalInfo.put("phone", value);
        else if (infoLine.contains("email") && !personalInfo.has("email"))
            personalInfo.put("email", value);
    }

    result.put("personal_info", personalInfo);
}
```

### Build and Deployment

```bash
mvn package -Dmaven.test.skip=true
sudo /opt/tomcat/bin/shutdown.sh
sudo rm -rf /opt/tomcat/webapps/ajirika
sudo rm -f /opt/tomcat/webapps/ajirika.war
sudo cp target/ajirika.war /opt/tomcat/webapps/
export JAVA_OPTS="-Xmx4g -Xms512m"
sudo -E /opt/tomcat/bin/startup.sh
```

The WAR size was 599MB, reflecting the inclusion of the CoreNLP models JAR. Deployment and model loading completed successfully. The application was accessible at http://localhost:8080/ajirika/processCV.jsp.

---

## Testing Process and Results

### Test Document

The same CV used in the standalone phase: a one-page cybersecurity student CV in PDF format, digitally created (not scanned), text-based. 303 words, one page.

### Test Procedure

1. Navigated to http://localhost:8080/ajirika/processCV.jsp in the browser
2. Selected the CV PDF using the file upload control
3. Clicked the Process CV button
4. Observed the Processing Logs tab and then the Results tab

### Pipeline Execution Trace

The Tomcat logs confirmed the following execution path:

1. File received and saved to Tomcat's temp directory
2. Tika parsed the PDF and produced structured text output with full metadata
3. readCV processed the Tika XML output through Jsoup, reconstructing paragraph structure
4. breakdownCV.extractCVData was called with the plain text
5. CoreNLP pipeline was initialised and annotated the full document
6. All entity mentions were logged to catalina.out
7. The JSON response was assembled and returned to the browser

### JSON Response Produced

```json
{
  "personal_info": {
    "name": "Nmap",
    "email": "mazibohoppo@proton.me"
  },
  "education": [],
  "experience": [
    {
      "position": "OSINT, Incident Response..."
    }
  ],
  "skills": [],
  "references": []
}
```

### Browser Results Tab

The Results tab populated with the personal info section. Name displayed as "Nmap" (incorrect). Email displayed as "mazibohoppo@proton.me" (correct). Education, skills, and references sections showed no entries due to section detection failures upstream of the CoreNLP layer.

---

## NLP Quality Evaluation

### CoreNLP Performance in Web Context

The CoreNLP layer performed identically to the standalone POC. The entity detection log confirmed all the same findings:

- Email: correctly identified (mazibohoppo@proton.me)
- Cities: Nairobi, Kinshasa correctly tagged
- Countries: Kenya, Democratic Republic of the Congo correctly tagged
- Dates: all six dates correctly identified
- Name: "UPAO MAZIBO" was not detected as PERSON; instead the first PERSON entity encountered was "Nmap", a security tool misclassified by the model

The name failure is the same limitation documented in Phase 1. African names that do not appear in CoreNLP's training corpus (Wall Street Journal and similar English news sources) receive no PERSON tag. The fallback to the first line also failed in this case because readCV's text reconstruction joined the header block into a single long line containing the name, phone, email, and social links together. The first-line heuristic therefore produced a line too long and inconsistent to use as a name.

### Section Detection Performance

The section detection failures observed in the logs were upstream of CoreNLP and attributable to the readCV text reconstruction approach. Tika with Jsoup merged multiple CV sections into single text blocks based on character length heuristics. As a result, the EDUCATION header ("A. EDUCATION") was embedded mid-sentence in a block that also contained the summary paragraph. The detectSectionHeader method, which checks for exact or near-exact keyword matches on short strings, could not match these compound blocks. The fallback line-by-line parser then misclassified most content into education or experience based on keyword inference rather than actual section structure.

This is a readCV and breakdownCV architecture issue, not a CoreNLP issue. CoreNLP's contribution to the pipeline is limited to the personal info extraction step and does not affect section detection.

### Summary of Accuracy

| Field | Method | Result |
|---|---|---|
| Email | CoreNLP (EMAIL entity) | Correct |
| Name | CoreNLP (PERSON entity) | Incorrect - "Nmap" assigned |
| Phone | Regex | Correct - not displayed due to rendering gap |
| Education | Rule-based section detection | Failed - section not isolated |
| Experience | Rule-based section detection | Partial - incorrect content assigned |
| Skills | Rule-based section detection | Failed - section not isolated |
| References | Rule-based section detection | Failed - mailto links misidentified |

---

## Challenges Encountered

| Challenge                                        | Root Cause                                                                                 | Resolution                                                                                                |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| PDFBox 3.x API breaking change                   | PDDocument.load(File) was removed in 3.0                                                   | Replaced with Loader.loadPDF(file) and added the Loader import                                            |
| Duplicate servlet URL mapping                    | Our new servlet and uploadProcess both mapped to /processCV                                | Deleted the new servlet entirely and integrated into the existing one                                     |
| CoreNLP not in pom.xml                           | Project used OpenNLP                                                                       | Added both stanford-corenlp core and models JARs as dependencies                                          |
| Compiler target Java 8 incompatible with CoreNLP | CoreNLP requires minimum Java 11                                                           | Updated maven.compiler.source and target to 11                                                            |
| NullPointerException on db.isValid()             | JNDI datasource not configured, db was null                                                | Added null check before isValid call                                                                      |
| NullPointerException on getUserPrincipal()       | No authenticated user during testing                                                       | Wrapped in try-catch with -1 fallback                                                                     |
| JNDI datasource lookup failure                   | PostgreSQL driver not in Tomcat lib                                                        | Copied postgresql JAR from Maven cache to /opt/tomcat/lib/                                                |
| Name assigned as "Nmap"                          | CoreNLP has no African name training data; first PERSON entity in text was a tool name     | Documented as fundamental limitation; requires custom NER model or rule-based pre-extraction              |
| Section detection failures                       | readCV merges CV sections into long compound blocks; detectSectionHeader cannot match them | Documented as an upstream architecture issue in readCV and breakdownCV                                    |
| WAR size 599MB                                   | CoreNLP models JAR is approximately 400MB                                                  | Expected and accepted for evaluation purposes; production deployment would require model hosting strategy |

---

## Lessons Learned

**CoreNLP is a domain-specific tool, not a universal NER solution.**
The model was trained on English news corpora. It performs accurately on the types of named entities that appear in news text: Western proper nouns, organisations, geographic locations, and dates. It has no training signal for African names, cybersecurity tool names used as skills, or CV-specific entity categories such as SKILL and CERTIFICATION.

**The name extraction problem is structural, not a tuning issue.**
No configuration change will make CoreNLP recognise "UPAO MAZIBO" as a PERSON without either retraining the NER model on African name data or applying a pre-extraction rule that identifies the candidate name before CoreNLP is invoked. The first-line heuristic approach is the correct fallback but requires readCV to produce clean line-separated output rather than merged blocks.

**Text reconstruction quality determines downstream NLP quality.**
The readCV class uses character length thresholds to decide whether consecutive text elements belong to the same paragraph. This heuristic works for flowing prose but fails for CV structure, where headers, bullet points, and section labels must be preserved as distinct lines. Improving readCV's reconstruction logic would benefit all downstream processing including both CoreNLP and the rule-based section parser.

**Integrating into an existing servlet is preferable to adding a new one.**
The existing uploadProcess servlet already handled multipart file upload, log capture, error handling, and JSON response formatting correctly. The correct integration surface was a single method in a single class, not a parallel servlet.

**WAR size management is necessary for CoreNLP in production.**
A 599MB WAR is acceptable for a local evaluation but unsuitable for CI/CD pipelines, rapid redeployment, or limited-storage environments. Production use would require either running CoreNLP as a separate process with the models JAR excluded from the WAR, or hosting the models externally.

**Heap configuration is mandatory and must be documented.**
CoreNLP will silently fail with an OutOfMemoryError on default Tomcat heap settings. Any deployment documentation for a CoreNLP-integrated Ajirika must specify the -Xmx4g JAVA_OPTS requirement explicitly.

---

## Future Recommendations for Ajirika

### Recommendation 1 - Fix readCV text reconstruction first

Before any NLP engine can produce accurate results on this CV structure, readCV must produce clean, line-separated output where section headers, institution names, and bullet points are on distinct lines rather than merged into compound blocks. This is a prerequisite for all downstream improvements and does not require any NLP work.

### Recommendation 2 - Add a name extraction rule upstream of CoreNLP

The candidate name is reliably the first non-empty line of a CV before the contact block. A simple rule that extracts the first line containing only alphabetic characters and spaces, with between two and five words, will correctly identify the name for the majority of CVs without requiring NER at all. CoreNLP can then be reserved for organisation, date, and location extraction where it performs reliably.

### Recommendation 3 - Use CoreNLP selectively for what it does well

Based on the evaluation, CoreNLP adds genuine value for: date and timeline extraction from education and experience sections, organisation name detection for Western company and university names, city and country tagging for location fields, and email address extraction as a reliable fallback. It should not be relied upon for name extraction on African CVs or for skills classification.

### Recommendation 4 - Train a custom OpenNLP NER model for African names

The project has already declared OpenNLP as its NLP library and has the training infrastructure in analyzeCV.java. Training a custom person NER model on a dataset of African names, including East African and Central African naming conventions, would solve the name recognition problem within the existing OpenNLP architecture. A dataset of 500 to 1000 annotated names in NER training format would be sufficient for a baseline model.

### Recommendation 5 - Consider a hybrid pipeline

The most practical production architecture combines rule-based pre-processing for name and section detection, CoreNLP for dates, organisations, cities, and countries, and the existing breakdownCV rule-based parsers for skills and references. No single approach handles all CV fields reliably. A layered pipeline that assigns each field to the method most suited to it will outperform any single-engine approach.

### Recommendation 6 - Evaluate transformer-based models for a future phase

Models such as bert-base-NER or spaCy with transformer backends significantly outperform both CoreNLP and OpenNLP on domain-specific and multilingual text. These are Python-ecosystem tools and would require a microservice bridge to communicate with the Java backend. This is higher effort but would represent a meaningful accuracy improvement, particularly for African name recognition and skills extraction.

---

## Environment Reference

| Component | Details |
|---|---|
| Machine | Lenovo ThinkPad |
| OS | Kali Linux (6.19.14+kali-amd64) |
| RAM | 16GB |
| IDE | VSCodium |
| Java Version | OpenJDK 25.0.3-ea |
| Maven Version | Apache Maven 3.9.12 |
| Tomcat Version | Apache Tomcat 10.1.55 |
| PostgreSQL Version | 18.3 |
| CoreNLP Version | 4.5.10 |
| PDFBox Version | 3.0.3 (standalone POC only) |
| Tika Version | 3.1.0 (web integration) |
| OpenNLP Version | 2.5.2 (existing, not replaced) |
| Test CV | One-page cybersecurity student CV, PDF, text-based, 303 words |

---

*Documentation produced as part of a cybersecurity and software engineering internship portfolio.*
*Tools: Stanford CoreNLP 4.5.10 - Apache Tika 3.1.0 - Apache OpenNLP 2.5.2 - Java 25 - Apache Maven 3.9.12 - Apache Tomcat 10.1.55 - PostgreSQL 18.3 - Kali Linux*