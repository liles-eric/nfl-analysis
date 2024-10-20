# Azure Folder

This folder contains Azure Data Factory-related JSON files for orchestrating pipelines, linking services, and managing datasets for the NFL analysis project. These JSON files represent resources such as datasets, linked services, and pipelines that are configured in Azure to automate the flow of data between different sources and destinations (such as Blob Storage, SQL databases, etc.).

## 1. Folder Structure

### 1.1 **dataset/**
Contains JSON files representing datasets used in Azure Data Factory pipelines. These datasets represent various types of data sources (e.g., NFL team stats, weather data) in Blob storage or SQL databases.

- **NFL_stadiums_weather.json**: Dataset for weather data of NFL stadiums.
- **NFL_stats_team_def_sql.json**: Dataset representing NFL team defensive stats stored in SQL.
- **nlf_def_team_stats.json**: Dataset for NFL defensive team statistics in Blob Storage.
- **nlf_stadium_weather_SQL.json**: Dataset for NFL stadium weather data stored in SQL.

### 1.2 **factory1/**
Contains the primary Azure Data Factory pipeline file, which is responsible for orchestrating the end-to-end flow of data.

- **nfl-data-pipeline.json**: This is the main Azure Data Factory pipeline used for moving data between Blob Storage and SQL databases. It includes tasks like copying data, transforming it, and loading it into the destination storage or database.

### 1.3 **linkedService/**
Contains JSON files representing Linked Services in Azure Data Factory. Linked Services define the connection information for external data sources like Blob Storage, SQL databases, and other services.

- **AzureBlobStorage1.json**: Linked Service to the first Azure Blob Storage account.
- **AzureBlobStorage2_nflstats.json**: Linked Service to the second Azure Blob Storage account specifically for NFL stats.
- **LinkedSQLSportsStatsv2.json**: Linked Service to the SQL database for sports stats.
- **nlf_misc_blob_linked.json**: Linked Service to another miscellaneous Blob Storage account.
- **SportsStatsSQLDB.json**: Linked Service to the main SQL Database for sports stats.
- **SportStatsSQLServerLinkv3.json**: Linked Service to the SQL Server in its third version, specifically for NFL sports stats.

### 1.4 **pipeline/**
Contains JSON files representing individual pipelines created in Azure Data Factory for various processes.

- **NLF-Misc-Pipeline.json**: A miscellaneous pipeline used for handling data processing tasks unrelated to the main NFL stats or weather pipelines.

---

## Usage
1. **Data Pipelines**: These pipelines handle moving NFL statistics and weather data from Azure Blob Storage into SQL databases.
2. **Linked Services**: The linked services provide connectivity to external storage and database systems required by the pipelines.
3. **Datasets**: Each dataset in the `dataset/` folder corresponds to a different source or destination dataset that the pipelines work with.
4. **Pipelines**: Use the JSON files in the `pipeline/` folder to orchestrate specific data flows within the Data Factory.

## Notes
- Refer to the individual dataset or linked service JSON files for more specific configuration details.
- The files here correspond to Azure Data Factory configuration and should be uploaded to your Data Factory environment to be operational.
