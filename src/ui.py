import os
import re
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display, Markdown, clear_output
from utils import compute_file_hash

def file_explorer(df_series_metadata ):
    file_dropdown = None
    file_map = {}
    tv_label_map = {}

    # ─────────────────────────────────────
    # STEP 1: Scan folder and extract file info
    raw_data_dir = "../data/raw/"

    # Matches: IBGE_20250329_151203_T6784-V9808_153017.csv
    filename_pattern = re.compile(
        r"(?P<source>IBGE|BCB)_(?P<session>\d{8}_\d{6})_T(?P<table>\d+)-V(?P<variable>\d+)_(?P<filetime>\d{6})\.csv"
    )

    records = []

    for fname in os.listdir(raw_data_dir):
        match = filename_pattern.match(fname)
        if match:
            rec = match.groupdict()
            rec["filename"] = os.path.join(raw_data_dir, fname)
            records.append(rec)

    df_all_files = pd.DataFrame(records)

    # Add combined column for selection
    df_all_files["T-V"] = "T" + df_all_files["table"] + "-V" + df_all_files["variable"]

    # ─────────────────────────────────────
    # STEP 2: Build UI widgets

    # Unique source list
    source_selector = widgets.Dropdown(
        options=sorted(df_all_files["source"].unique()),
        value="IBGE",
        description="Source:"
    )

    # Will be filled dynamically
    tv_selector = widgets.Dropdown(
        options=[],
        description="Table-Var:"
    )

    series_name_label = widgets.HTML("<b>Series Name:</b> (will update on selection)")


    # Output area to display results
    result_output = widgets.Output()

    # ─────────────────────────────────────
    # STEP 3: UI logic to update dropdowns and show table

    def update_tv_options(change):
        selected_source = change["new"]
        # Filter files by source
        filtered = df_all_files[df_all_files["source"] == selected_source].copy()

        # Ensure table and variable are integers for joining
        filtered["table"] = filtered["table"].astype(int)
        filtered["variable"] = filtered["variable"].astype(int)

        # Merge with metadata to get series name
        merged = filtered.merge(
            df_series_metadata.reset_index(),  # Ensure 'name' is available
            how="left",
            on=["table", "variable"]
        )

        # Create a label like: T1234-V5678 | My Series Name
        merged["tv_label"] = merged.apply(
            lambda row: f"T{row['table']}-V{row['variable']} | {row['name'] if pd.notna(row['name']) else '(Unnamed)'}",
            axis=1
        )

        # Map: display label → actual T-V code
        tv_label_map.clear()
        tv_label_map.update(dict(zip(merged["tv_label"], merged["T-V"])))

        # Set dropdown options to the labels
        tv_selector.options = sorted(tv_label_map.keys(), key=lambda s: s.split(" | ", 1)[1])

        # Select the first one by default
        if tv_selector.options:
            tv_selector.value = tv_selector.options[0]


    # Container for dropdown and plot
    file_selector_container = widgets.VBox()
    file_plot_output = widgets.Output()
    filename_label = widgets.HTML("<b>Selected file:</b> (will appear here)")
    def show_files_table(change):
        nonlocal file_dropdown, file_map
        # Try to look up the name using table and variable


        with result_output:
            clear_output()
            file_selector_container.children = []  # Reset

            source = source_selector.value
            tv = tv_label_map[tv_selector.value]
            filtered = df_all_files[
                (df_all_files["source"] == source) & 
                (df_all_files["T-V"] == tv)
            ].copy()
            
            try:
                meta_row = df_series_metadata[
                    (df_series_metadata["table"] == int(tv.split("-")[0][1:])) &
                    (df_series_metadata["variable"] == int(tv.split("-")[1][1:]))
                ].iloc[0]
                series_name_label.value = f"Series Name: {meta_row.name}"
            except:
                series_name_label.value = "Series Name: (not found)"

            if filtered.empty:
                display(widgets.HTML("No files found for selected source and series."))
                return

            # Compute hash
            filtered["file_hash"] = filtered["filename"].apply(compute_file_hash)
            def get_valor_bounds(filepath):
                try:
                    df = pd.read_csv(filepath, usecols=["valor"])
                    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
                    df = df.dropna()
                    if df.empty:
                        return (np.nan, np.nan)
                    return (df.iloc[0]["valor"], df.iloc[-1]["valor"])
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    return (np.nan, np.nan)

            # Apply to each file
            filtered[["valor_first", "valor_last"]] = filtered["filename"].apply(
                lambda path: pd.Series(get_valor_bounds(path))
            )
            # Generate label for each option
            filtered["label"] = filtered.apply(
                lambda row: f"{row['session']} - {row['filetime']} - "
                            f"{row['file_hash'][:4]}...{row['file_hash'][-4:]} | "
                            f"valor: {row['valor_first']:.2f} → {row['valor_last']:.2f}",
                axis=1
            )
            # Map labels to filenames
            filtered = filtered.sort_values(by=["session", "filetime"], ascending=False)
            file_map = dict(zip(filtered["label"], filtered["filename"]))

            # Create dropdown
            file_dropdown = widgets.Select(
                options=list(file_map.keys()),
                description="File:",
                layout=widgets.Layout(width="700px", height="150px")
            )
            # Define plot function
            def plot_selected_file(change):

                with file_plot_output:
                    clear_output()
                    selected_label = change["new"]
                    file_path = file_map[selected_label]
                    filename_label.value = f"Selected file: {file_path}"

                    try:
                        df = pd.read_csv(file_path)
                        if "data" in df.columns:
                            df["data"] = pd.to_datetime(df["data"], errors="coerce")
                        if "valor" in df.columns:
                            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

                            # Plot
                            sns.set_theme()
                            sns.set_context("notebook")
                            plt.figure(figsize=(12, 6))
                            sns.lineplot(data=df, x="data", y="valor")
                            plt.xlabel("Date")
                            plt.ylabel("Value")
                            plt.title(f"{source} {tv} - {selected_label}")
                            sns.despine()
                            plt.tight_layout()
                            plt.show()
                        else:
                            print("Column 'valor' not found.")
                    except Exception as e:
                        print(f"Error reading or plotting file: {e}")   

            # Now register observer AFTER triggering initial plot
            file_dropdown.observe(plot_selected_file, names="value")

            plot_selected_file({"new": file_dropdown.value})

            # Add widgets to UI
            file_selector_container.children = [file_dropdown, file_plot_output]
            display(file_selector_container)
            
    # Attach logic
    source_selector.observe(update_tv_options, names="value")
    tv_selector.observe(show_files_table, names="value")

    # Initialize dropdowns
    update_tv_options({"new": source_selector.value})
    show_files_table(None)

    # ─────────────────────────────────────
    # Display full UI
    display(widgets.VBox([
        widgets.HTML("<h3>🔎 Analyze All Files by Source and Series</h3>"),
        source_selector,
        tv_selector,
        series_name_label,   
        filename_label, 
        result_output,

    ]))

    return {
        "get_selected_file": lambda: file_map[file_dropdown.value] if file_dropdown else None,
        "file_dropdown": file_dropdown,
        "file_map": file_map
    }


import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown
from utils import delete_old_raw_versions

def raw_cleanup_widget():
    """
    Widget interface to delete old raw CSV and JSON files in ../data/raw/.
    Includes confirmation step before deletion.
    """
    # Output areas
    confirmation_output = widgets.Output()
    result_output = widgets.Output()

    # Delete button
    delete_button = widgets.Button(
        description="🧹 Delete old raw CSV and JSON files",
        button_style="danger"
    )

    # Confirmation buttons
    confirm_button = widgets.Button(description="Yes, delete", button_style="danger")
    cancel_button = widgets.Button(description="Cancel", button_style="")

    # Horizontal layout
    confirmation_box = widgets.HBox([confirm_button, cancel_button])

    # Step 1: Ask for confirmation
    def on_delete_button_click(b):
        with confirmation_output:
            clear_output()
            display(Markdown("⚠️ Are you sure you want to delete old versions of raw data files?"))
            display(confirmation_box)

    # Step 2: Confirm and delete
    def on_confirm_click(b):
        with confirmation_output:
            clear_output()
            display(Markdown("🧼 Deleting files..."))

        deleted = delete_old_raw_versions()

        with result_output:
            clear_output()
            if deleted:
                display(Markdown(f"✅ **{len(deleted)} file(s) deleted:**"))
                for f in deleted:
                    display(Markdown(f"- `{f}`"))
            else:
                display(Markdown("✅ No old files to delete. All clean!"))

    # Step 3: Cancel
    def on_cancel_click(b):
        with confirmation_output:
            clear_output()
            display(Markdown("❎ Deletion canceled."))

    # Link buttons to actions
    delete_button.on_click(on_delete_button_click)
    confirm_button.on_click(on_confirm_click)
    cancel_button.on_click(on_cancel_click)

    # Display everything
    display(widgets.VBox([
        delete_button,
        confirmation_output,
        result_output
    ]))

def plot_columns_selector(df):
    # Ensure 'data' column is datetime
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    # Extract Y columns (exclude 'data')
    y_columns = df.columns.drop("data")

    # Create SelectMultiple widget
    column_selector = widgets.SelectMultiple(
        options=y_columns,
        description="Y columns:",
        layout=widgets.Layout(width='250px', height='300px')
    )

    # Output area for the plot
    plot_output = widgets.Output()

    # Define the update function
    def update_plot(change):
        with plot_output:
            clear_output(wait=True)
            selected_cols = list(column_selector.value)
            if selected_cols:
                plt.figure(figsize=(12, 6))
                sns.set_theme()
                for col in selected_cols:
                    plt.plot(df["data"], df[col], label=col)
                plt.xlabel("Date")
                plt.ylabel("Value")
                plt.title("Selected Series")
                plt.legend()
                plt.tight_layout()
                plt.show()
            else:
                print("Select at least one column to display.")

    # Attach the observer
    column_selector.observe(update_plot, names="value")

    # Trigger an initial plot
    update_plot({"new": column_selector.value})

    # Layout side-by-side
    ui = widgets.HBox([
        column_selector,
        plot_output
    ])
    display(ui)