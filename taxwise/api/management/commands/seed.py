import pandas as pd
import tabula
from django.core.management.base import BaseCommand

from taxwise.api.models import ChapterSection, Tarriff


class Command(BaseCommand):
    """
    This command will create a base32 secret for the user, and show a QR code for scanning.
    """

    help = "Generate TOTP code for use with TOTP login"

    def generate_tarriffs(self):
        # Read pdf into DataFrame
        list_of_df = tabula.read_pdf("zimra.pdf", pages="18-20")

        columns = []

        # print(list_of_df)

        for idx, df in enumerate(list_of_df):

            if isinstance(df, pd.DataFrame):
                print(f"Page number : {idx} has {len(df.columns)} columns")
                # print(df)

                columns.append(len(df.columns))

                if len(df.columns) == 5:
                    # Type one page

                    df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "General"]
                elif len(df.columns) == 6:
                    # Type one page
                    df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "General", "Other Column"]

                for row in df.iterrows():
                    data = row[1]
                    # print('********************************************************************************************************')
                    # print(data)
                    # print('********************************************************************************************************')

                    if data.Heading == "Heading":
                        # print("****** header row ******")
                        # print(data)
                        # print('********************************************************************************************************')
                        continue
                    if data.value_counts().size == 2:
                        # print("****** sub-heading row ******")
                        # print(data)
                        print("****** sub-heading row ******")
                        if data.Heading and data.Heading != 'Heading' and str(data.Heading) != 'nan':
                            print(data)
                            chapter_section = ChapterSection(
                                chapter=str(data["Heading"]).split(".")[0],
                                section=data["Heading"],
                                description=data["Description"],
                            )
                            chapter_section.save()
                            print('********************************************************************************************************')
                        # print('********************************************************************************************************')
                        continue
                    else:
                        print("****** tarriff row ******")
                        print(data)

                        tarriff = Tarriff(
                            heading=data["Heading"],
                            commodity_code=data["Commodity Code"],
                            description=data["Description"],
                            statistical_unit=data["Quantity"],
                            general_rate_of_duty=data["General"],
                            mtf_rate_of_duty=data["General"],
                        )
                        tarriff.save()
                        print(
                            "********************************************************************************************************"
                        )
                        continue
            else:
                print(f"Skipping Page number : {idx}")
                continue

        print("unique columns : %s", set(columns))

        # print(list_of_df)
        count = 0

        for idx, df in enumerate(list_of_df):
            if count > 10:
                break

            if isinstance(df, pd.DataFrame):
                print(f"Page number : {idx} has {len(df.columns)} columns")
                # print(df)

                columns.append(len(df.columns))

                if len(df.columns) == 5:
                    # Type one page

                    df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "General"]
                elif len(df.columns) == 6:
                    # Type one page
                    df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "General", "Other Column"]

                elif len(df.columns) == 10:
                    # Type 2
                    df.columns = [
                        "heading",
                        "CD",
                        "article_description",
                        "statistical_unit",
                        "general_rate_of_duty",
                        "eu_rate_of_duty",
                        "efta_rate_of_duty",
                        "sadc_rate_of_duty",
                        "unknown_1",
                        "mercosur_rate_of_duty",
                    ]

                elif len(df.columns) == 12:
                    # Type 3
                    df.columns = [
                        "heading",
                        "CD",
                        "article_description",
                        "statistical_unit",
                        "general_rate_of_duty",
                        "eu_rate_of_duty",
                        "efta_rate_of_duty",
                        "sadc_rate_of_duty",
                        "unknown_1",
                        "mercosur_rate_of_duty",
                        "unknown_2",
                        "unknown_3",
                    ]

                for row in df.iterrows():
                    data = row[1]
                    # print('********************************************************************************************************')
                    # print(data)
                    # print('********************************************************************************************************')

                    if data.Heading == "Heading":
                        # print("****** header row ******")
                        # print(data)
                        # print('********************************************************************************************************')
                        continue
                    if data.value_counts().size == 2:
                        # print("****** sub-heading row ******")
                        # print(data)
                        # print('********************************************************************************************************')
                        continue
                    else:
                        print("****** tarriff row ******")
                        print(data)
                        print(
                            "********************************************************************************************************"
                        )
                        continue
            else:
                print(f"Skipping Page number : {idx}")
                continue

        print("unique columns : %s", set(columns))

    def handle(self, *args, **options):
        self.stdout.write("Seeding tarriffs...")
        self.generate_tarriffs()
        self.stdout.write("Tarriffs saved !!!")
