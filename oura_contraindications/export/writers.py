import pandas as pd


def save_as_xlsx(df, file, index=True, **to_excel_kwargs):
    """
    Save dataframe as .xlsx file with dates properly formatted

    :param df: dataframe to save
    :type df: df object

    :param file: File path
    :type file: string

    :param index: save df index, in this case summary_date
    :type index: Boolean
    """

    def localize(df):
        """
        Remove tz from datetime cols since Excel doesn't allow
        """
        tz_cols = df.select_dtypes(include=["datetimetz"]).columns
        for tz_col in tz_cols:
            df[tz_col] = df[tz_col].dt.tz_localize(None)
        return df

    import xlsxwriter

    df = df.copy()
    df = localize(df)
    with pd.ExcelWriter(
        file,
        engine="xlsxwriter",
        date_format="m/d/yyy",
        datetime_format="m/d/yyy h:mmAM/PM",
    ) as writer:
        df.to_excel(writer, index=index, **to_excel_kwargs)


def tableize(df, tablefmt="pretty", is_print=True):
    """
    Converts dataframe to a formatted table
    For more details, see https://pypi.org/project/tabulate/

    :param df: dataframe to save
    :type df: df object

    :param tablefmt: format of table
    :type tablefmt: string

    :param is_print: print to standard output?
    :type is_print: boolean
    """
    from tabulate import tabulate

    table = tabulate(
        df,
        headers="keys",
        tablefmt=tablefmt,
        showindex=True,
        stralign="center",
        numalign="center",
    )
    if is_print:
        print(table)
    return table
