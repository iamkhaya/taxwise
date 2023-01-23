import pandas as pd
import tabula
from django.core.management.base import BaseCommand
from tabulate import tabulate
from taxwise.api.models import ChapterSection, Tarriff


class Command(BaseCommand):
    """
    This command will create a base32 secret for the user, and show a QR code for scanning.
    """

    help = "Generate TOTP code for use with TOTP login"

    PDF_FILE_NAME = "zimra-2022.pdf"
    PDF_PAGE_RANGE = "990-1050"

    def map_columns(self, num_columns):
        # if num_columns == 4:
        #     return ["Commodity Code", "Description", "Quantity", "General"]
        if num_columns == 5:
            return ["Heading", "Commodity Code", "Description", "Quantity", "MFN"]
        elif num_columns == 6:
            return ["Heading", "Commodity Code", "Description", "Quantity", "General", "MFN"]
        elif num_columns == 7:
            return ["Heading", "Commodity Code", "Description", "Unamed", "Quantity", "General", "MFN"]
        # elif num_columns == 8:
        #     return ["Heading", "Commodity Code", "Description", "Quantity", "General", "MFN", "Other", "Other"]

        else:
            raise ValueError(f"Invalid number of columns: {num_columns}")

    def _process_type_1_row(self, row: pd.Series):
        """
        Process Type 1 type
        """
        print("****** start : tarriff row type 1******")

        row = row.dropna()

        print("****** end : tarriff row type 1******")

        tarriff = Tarriff(
            heading=row.get("Heading"),
            commodity_code=row.get("Commodity Code", ""),
            description=row.get("Description", ""),
            statistical_unit=row.get("Quantity", ""),
            general_rate_of_duty=row.get("General", ""),
            mtf_rate_of_duty=row.get("MFN", ""),
        )
        tarriff.save()

    def _process_type_2_row(self, row: pd.Series):
        """
        Process Type 1 type
        """
        print("****** start : tarriff row type 2 ******")
        print(row)

        row = row.dropna()
        # print(row)

        general = ""
        unit = ""
        if row.get("Quantity"):
            digits = [(i, c) for i, c in enumerate(row.get("Quantity")) if c.isdigit()]
            print("-- digits :" + str(digits))
            print("qty : " + row.get("Quantity"))

            if len(digits) > 1:
                general = row.get("Quantity")[digits[1][0] :]
                unit = row.get("Quantity")[: 1 * digits[1][0]]

        tarriff = Tarriff(
            heading=row.get("Heading"),
            commodity_code=row.get("Commodity Code", ""),
            description=row.get("Description", ""),
            statistical_unit=unit or row.get("Quantity", ""),
            general_rate_of_duty=row.get("General", "") or general,
            mtf_rate_of_duty=row.get("MFN", ""),
        )
        tarriff.save()

    def _process_type_3_row(self, row: pd.Series):
        """
        Process Type 3 type
        """
        print("****** start : tarriff row type 2 ******")
        print(row)

        row = row.dropna()
        print(row)

        tarriff = Tarriff(
            heading=row.get("Heading"),
            commodity_code=row.get("Commodity Code", ""),
            description=row.get("Description", ""),
            statistical_unit=row.get("Quantity"),
            general_rate_of_duty=row.get("General"),
            mtf_rate_of_duty=row.get("MFN", ""),
        )
        tarriff.save()

    def _process_type_4_row(self, row: pd.Series):
        """
        Process Type 4 type
        """
        print("****** start : tarriff row type 2 ******")
        print(row)

        row = row.dropna()
        print(row)

        general = ""
        unit = ""
        if row[2]:
            digits = [(i, c) for i, c in enumerate(row[2]) if c.isdigit()]
            print("-- digits :" + str(digits))
            print("qty : " + row.get("Quantity"))

            if len(digits) > 1:
                general = row.get("Quantity")[digits[1][0] :]
                unit = row.get("Quantity")[: 1 * digits[1][0]]

        tarriff = Tarriff(
            heading=row[0],
            commodity_code=row[0],
            description=row[1],
            statistical_unit=unit or row[2],
            general_rate_of_duty=row[3] or general,
            mtf_rate_of_duty=row[4],
        )
        tarriff.save()

    def _process_section_header_row(self, row: pd.Series):
        """
        Process Type 3 type
        """

        if row.get("Heading") and row.Heading != "Heading" and str(row.Heading) != "nan":
            print("****** section row ******")
            print(row)
            chapter_section = ChapterSection(
                chapter=str(row.get("Heading")).split(".")[0],
                section=row.get("Heading"),
                description=row.get("Description"),
            )
            chapter_section.save()

    def _write_axes(self, df):
        """
        Write Axes
        """
        # write axes
        # ['0104.10.10', '- - -Pure-bred breeding sheep', '1. Kg', '0%', '0%.1']
        if len(df.columns) == 4:
            print(df.axes[1].tolist())
            tarriff = Tarriff(
                heading=df.axes[1].tolist()[0],
                commodity_code=df.axes[1].tolist()[1],
                description=df.axes[1].tolist()[2],
                statistical_unit=df.axes[1].tolist()[3],
                general_rate_of_duty=df.axes[1].tolist()[3],
                # mtf_rate_of_duty=data[5],
            )
            tarriff.save()

    def _get_page_type(self, number_of_columns: int):

        if number_of_columns == 5:
            return "type_1"
        elif number_of_columns == 6:
            return "type_2"
        elif number_of_columns == 7:
            return "type_3"

        else:
            raise ValueError(f"Unknown type with: {number_of_columns} columns")

    def process_page_data(self, df):
        """
        Process the page
        """
        page_type = self._get_page_type(number_of_columns=len(df.columns))

        try:
            df.columns = self.map_columns(len(df.columns))
        except ValueError:
            print("skipping page : it has " + str(len(df.columns)) + "columns")

        for row in df.iterrows():
            data = row[1]

            if "No." in data.index.values or "Heading" in data.index.values:

                print("****** data row ******")
                # print(data)
                print("type : " + str(type(row[1])))
                print("**********************")

                if page_type == "type_1":
                    self._process_type_1_row(data)
                elif page_type == "type_2":
                    self._process_type_2_row(data)
                elif page_type == "type_3":
                    self._process_type_3_row(data)

    def generate_tarriffs(self):
        try:
            list_of_df = tabula.read_pdf(self.PDF_FILE_NAME, pages=self.PDF_PAGE_RANGE)
            tabula.convert_into(
                self.PDF_FILE_NAME, "test.csv", output_format="csv", stream=True, pages=self.PDF_PAGE_RANGE
            )

            # print(list_of_df)
        except Exception as e:
            print(f"An error occurred while reading the pdf file: {e}")
            return

        for idx, df in enumerate(list_of_df):
            if isinstance(df, pd.DataFrame):
                print(f"Page number : {idx} has {len(df.columns)} columns")
                print(df.axes[1].tolist())
                print(tabulate(df, headers="keys", tablefmt="psql"))
                # print(df)

                print("---------------------------------")
                self.process_page_data(df)

    def handle(self, *args, **options):
        self.stdout.write("Seeding tarriffs...")
        self.generate_tarriffs()
        self.stdout.write("\n\nTarriffs saved !!!")
