# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DATABOX.
#
# SENAITE.DATABOX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

PROJECTNAME = "senaite.databox"

TMP_FOLDER_KEY = "senaite.databox.tmp"

DATE_INDEX_TYPES = ["DateIndex"]

UID_CATALOG = "uid_catalog"

PARENT_TYPES = {
    "Analysis": "AnalysisRequest",
    "AnalysisRequest": "Client",
    "Contact": "Client",
    "ARReport": "AnalysisRequest",
    "Batch": "AnalysisRequest",
}

# TODO: Move to registry config
IGNORE_FIELDS = [
    "allowDiscussion",
    "contributors",
    "creators",
    "effectiveDate",
    "expirationDate",
    "language",
    "location",
    "rights",
    "subject",
]

IGNORE_CATALOG_IDS = [
    "auditlog_catalog"
]

# NOTE: Visible types are commented
NON_QUERYABLE_TYPES = [
    # "ARReport",
    # "ARTemplate",
    "ARTemplates",
    "ATBooleanCriterion",
    "ATCurrentAuthorCriterion",
    "ATDateCriteria",
    "ATDateRangeCriterion",
    "ATListCriterion",
    "ATPathCriterion",
    "ATPortalTypeCriterion",
    "ATReferenceCriterion",
    "ATRelativePathCriterion",
    "ATSelectionCriterion",
    "ATSimpleIntCriterion",
    "ATSimpleStringCriterion",
    "ATSortCriterion",
    # "AetiologicAgent",
    "AetiologicAgents",
    # "Analysis",
    "AnalysisCategories",
    # "AnalysisCategory",
    # "AnalysisProfile",
    "AnalysisProfiles",
    # "AnalysisRequest",
    "AnalysisRequestsFolder",
    # "AnalysisService",
    "AnalysisServices",
    # "AnalysisSpec",
    "AnalysisSpecs",
    # "Attachment",
    # "AttachmentType",
    "AttachmentTypes",
    "AuditLog",
    # "AutoImportLog",
    # "Batch",
    "BatchFolder",
    # "BatchLabel",
    "BatchLabels",
    "BikaSetup",
    # "Calculation",
    "Calculations",
    # "CaseOutcome",
    "CaseOutcomes",
    # "CaseStatus",
    "CaseStatuses",
    # "CaseSyndromicClassification",
    "CaseSyndromicClassifications",
    # "Client",
    "ClientFolder",
    # "Contact",
    # "Container",
    # "ContainerType",
    "ContainerTypes",
    "Containers",
    # "DataBox",
    "DataBoxFolder",
    # "Department",
    "Departments",
    # "Disease",
    "Diseases",
    # "Doctor",
    "Doctors",
    "Document",
    # "Drug",
    # "DrugProhibition",
    "DrugProhibitions",
    "Drugs",
    # "DuplicateAnalysis",
    # "DynamicAnalysisSpec",
    "DynamicAnalysisSpecs",
    "Ethnicities",
    # "Ethnicity",
    "Event",
    "File",
    "Folder",
    # "IdentifierType",
    "IdentifierTypes",
    "Image",
    # "Immunization",
    "Immunizations",
    # "Instrument",
    "InstrumentCalibration",
    # "InstrumentCertification",
    # "InstrumentLocation",
    "InstrumentLocations",
    # "InstrumentMaintenanceTask",
    # "InstrumentScheduledTask",
    # "InstrumentType",
    "InstrumentTypes",
    # "InstrumentValidation",
    "Instruments",
    "InsuranceCompanies",
    # "InsuranceCompany",
    # "Invoice",
    # "LabContact",
    "LabContacts",
    # "LabProduct",
    "LabProducts",
    "Laboratory",
    "Link",
    # "Manufacturer",
    "Manufacturers",
    # "Method",
    "Methods",
    # "Multifile",
    "News Item",
    # "Patient",
    "Patients",
    "Plone Site",
    # "Preservation",
    "Preservations",
    # "Pricelist",
    "PricelistFolder",
    # "ReferenceAnalysis",
    # "ReferenceDefinition",
    "ReferenceDefinitions",
    # "ReferenceSample",
    "ReferenceSamplesFolder",
    # "ReflexRule",
    "ReflexRuleFolder",
    "RejectAnalysis",
    # "Report",
    "ReportFolder",
    # "SampleCondition",
    "SampleConditions",
    "SampleMatrices",
    # "SampleMatrix",
    # "SamplePoint",
    "SamplePoints",
    # "SampleType",
    "SampleTypes",
    # "SamplingDeviation",
    "SamplingDeviations",
    # "StorageContainer",
    # "StorageFacility",
    # "StorageLocation",
    "StorageLocations",
    "StorageRootFolder",
    "StorageSamplesContainer",
    # "SubGroup",
    "SubGroups",
    # "Supplier",
    "SupplierContact",
    "Suppliers",
    # "SupplyOrder",
    "SupplyOrderFolder",
    # "Symptom",
    "Symptoms",
    "TempFolder",
    "Topic",
    # "Treatment",
    "Treatments",
    # "VaccinationCenter",
    "VaccinationCenterContact",
    "VaccinationCenters",
    # "Worksheet",
    "WorksheetFolder",
    # "WorksheetTemplate",
    "WorksheetTemplates",
]
