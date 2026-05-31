from __future__ import annotations

SOURCE_TOPIC = "diabetes"

HEALTHCARE_SOURCES = [
    {
        "name": "MedlinePlus Type 2 Diabetes",
        "url": "https://medlineplus.gov/diabetestype2.html",
        "type": "condition_overview",
        "source_owner": "NIH National Library of Medicine",
        "priority": 1,
    },
    {
        "name": "CDC Diabetes Basics",
        "url": "https://www.cdc.gov/diabetes/about/index.html",
        "type": "condition_overview",
        "source_owner": "CDC",
        "priority": 1,
    },
    {
        "name": "CDC Diabetes Symptoms",
        "url": "https://www.cdc.gov/diabetes/signs-symptoms/index.html",
        "type": "symptoms",
        "source_owner": "CDC",
        "priority": 1,
    },
    {
        "name": "CDC Diabetes Testing",
        "url": "https://www.cdc.gov/diabetes/diabetes-testing/index.html",
        "type": "diagnosis_testing",
        "source_owner": "CDC",
        "priority": 1,
    },
    {
        "name": "NIDDK Diabetes Overview",
        "url": "https://www.niddk.nih.gov/health-information/diabetes/overview",
        "type": "condition_overview",
        "source_owner": "NIH NIDDK",
        "priority": 1,
    },
    {
        "name": "NIDDK Symptoms and Causes of Diabetes",
        "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/symptoms-causes",
        "type": "symptoms_causes",
        "source_owner": "NIH NIDDK",
        "priority": 1,
    },
    {
        "name": "NIDDK Diabetes Tests and Diagnosis",
        "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis",
        "type": "diagnosis_testing",
        "source_owner": "NIH NIDDK",
        "priority": 1,
    },
    {
        "name": "Mayo Clinic Diabetes Symptoms and Causes",
        "url": "https://www.mayoclinic.org/diseases-conditions/diabetes/symptoms-causes/syc-20371444",
        "type": "symptoms_causes",
        "source_owner": "Mayo Clinic",
        "priority": 2,
    },
    {
        "name": "Mayo Clinic Diabetes Diagnosis and Treatment",
        "url": "https://www.mayoclinic.org/diseases-conditions/diabetes/diagnosis-treatment/drc-20371451",
        "type": "diagnosis_treatment",
        "source_owner": "Mayo Clinic",
        "priority": 2,
    },
    {
        "name": "Cleveland Clinic Diabetes",
        "url": "https://my.clevelandclinic.org/health/diseases/7104-diabetes",
        "type": "condition_overview",
        "source_owner": "Cleveland Clinic",
        "priority": 2,
    },
    {
        "name": "American Diabetes Association Diagnosis",
        "url": "https://diabetes.org/about-diabetes/diagnosis",
        "type": "diagnosis_testing",
        "source_owner": "American Diabetes Association",
        "priority": 2,
    },
    {
        "name": "American Heart Association Diabetes Overview",
        "url": "https://www.heart.org/en/health-topics/diabetes/about-diabetes",
        "type": "condition_overview",
        "source_owner": "American Heart Association",
        "priority": 3,
    },
]


def source_urls() -> list[str]:
    return [source["url"] for source in HEALTHCARE_SOURCES]
