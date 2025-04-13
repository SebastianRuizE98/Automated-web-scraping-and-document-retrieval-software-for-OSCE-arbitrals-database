# Automated-web-scraping-and-document-retrieval-software-for-OSCE-arbitrals-database
This project consisted of the development of an automated web scraping and document retrieval software for the OSCE arbitrals database, which contains 699 records divided across multiple pages. This database also included download links for documents providing details about each arbitral case, including results and resolutions.

Why is it useful?
- It allows data to be consolidated into a single XLSX file, enabling further actions and analysis to gain deeper insights.
- It performs automatic downloads at short intervals, significantly saving time.
- It ensures consistency and reduces human error in the data collection process.
- It facilitates large-scale monitoring of arbitration outcomes and trends over time.
- It supports the generation of reports or dashboards for decision-making and transparency.
- It enables researchers, legal analysts, or policymakers to access structured data more efficiently.

Process:
- A script was developed to automatically download the tables and export them to an XLSX file.
- Another script was created to automatically download the documents from the database.
- A pattern in the href attribute of the download buttons was identified, which made it possible to rename the downloaded files for easier recognition.
- Finally, I obtained a downloaded database in CSV format along with the corresponding documents for each record.

  --> You can check the raw data in the CSV file located in the folder, as well as a screenshot showing the documents organized in numerical order.

