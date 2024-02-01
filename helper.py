from LinkedIn_Jobs import jobs_scrapper
import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe


def export_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)


def export_to_google_sheets(dataframe, sheet_name):
    gc = gspread.service_account()  # Use your own credentials
    sh = gc.create(sheet_name)
    worksheet = sh.get_worksheet(0)
    set_with_dataframe(worksheet, dataframe)


# Streamlit app
def main():
    st.title("LinkedIn Jobs")

    # Input box for URL
    url = st.text_input("Enter the URL:", "https://example.com")

    # Button to trigger scraping
    if st.button("Scrape Data"):
        # Call the scrape_data function with the entered URL
        scraped_data = jobs_scrapper(url)

        # Display the scraped data
        st.write("Scraped Data:")
        st.write(scraped_data)

        # Export options
        export_format = st.selectbox("Select export format:", ["CSV", "Google Sheets"])

        if export_format == "CSV":
            # Download button for CSV
            st.download_button(
                label="Download CSV",
                data=scraped_data.to_csv(index=False).encode(),
                file_name="scraped_data.csv",
                key="csv_download_button"
            )
        elif export_format == "Google Sheets":
            # Input box for Google Sheets sheet name
            sheet_name = st.text_input("Enter Google Sheets sheet name:")

            # Download button for Google Sheets
            st.download_button(
                label="Export to Google Sheets",
                data="Exporting...",
                key="google_sheets_download_button",
                on_click=lambda: export_to_google_sheets(scraped_data, sheet_name)
            )


if __name__ == "__main__":
    main()
