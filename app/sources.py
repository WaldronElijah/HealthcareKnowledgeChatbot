from __future__ import annotations

HEALTHCARE_SOURCES = [
    {
        "name": "MedlinePlus Health Topics",
        "url": "https://medlineplus.gov/healthtopics.html",
        "type": "health_topic_index",
        "source_owner": "NIH National Library of Medicine",
        "priority": 1,
    },
    {
        "name": "MedlinePlus All Health Topics",
        "url": "https://medlineplus.gov/all_healthtopics.html",
        "type": "health_topic_index",
        "source_owner": "NIH National Library of Medicine",
        "priority": 1,
    },
    {
        "name": "CDC Health Topics",
        "url": "https://www.cdc.gov/health-topics.html",
        "type": "public_health_index",
        "source_owner": "CDC",
        "priority": 1,
    },
    {
        "name": "CDC FastStats Diseases and Conditions",
        "url": "https://www.cdc.gov/nchs/fastats/diseases-and-conditions.htm",
        "type": "statistics_reference",
        "source_owner": "CDC NCHS",
        "priority": 1,
    },
    {
        "name": "Mayo Clinic Diseases and Conditions",
        "url": "https://www.mayoclinic.org/diseases-conditions",
        "type": "condition_library",
        "source_owner": "Mayo Clinic",
        "priority": 2,
    },
    {
        "name": "Cleveland Clinic Diseases and Conditions",
        "url": "https://my.clevelandclinic.org/health/diseases",
        "type": "condition_library",
        "source_owner": "Cleveland Clinic",
        "priority": 2,
    },
    {
        "name": "WebMD Health Topics",
        "url": "https://www.webmd.com/a-to-z-guides/health-topics",
        "type": "consumer_health_library",
        "source_owner": "WebMD",
        "priority": 3,
    },
    {
        "name": "WebMD Medical Reference",
        "url": "https://www.webmd.com/a-to-z-guides/medical-reference/default.htm",
        "type": "consumer_medical_reference",
        "source_owner": "WebMD",
        "priority": 3,
    },
]


def source_urls() -> list[str]:
    return [source["url"] for source in HEALTHCARE_SOURCES]
