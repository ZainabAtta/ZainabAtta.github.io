from shiny import App, ui, render, reactive, req
from helper_text import tr, t, dnt, dnt_yaxis, t_age, gt, info_modal, forside_text, forside_icon_html, kontakt_info, group_translations,  group_to_columns, display_names, info_modal_title, display_names_yaxis, rettigheder, translations, fit, texts, display_name_translated, display_names_yaxis_translated
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px
from collections import OrderedDict
import folium
import statsmodels.api as sm
import plotly.io as pio



def load_dataset():
    try:
        df = pd.read_csv("/Users/zsa/Desktop/Speciale/Dashboard/data/data_2007_2022_collapse_Sundhedsraad_year_ver2.csv") 
        return df
    except Exception as e:
        print("Failed to load dataset:", e)
        return None


dataset = load_dataset()


geo_df = gpd.read_file("/Users/zsa/Desktop/Speciale/Dashboard/kode2/mapgeo.geojson")
geo_df["id"] = geo_df["id"].astype(str)
dataset["Sundhedsråd_kode"] = dataset["Sundhedsråd_kode"].astype(str)


combined_data = geo_df.merge(dataset, left_on="id", right_on="Sundhedsråd_kode", how="left")



if dataset is not None and "year" in dataset.columns:
    column_choices = [col for col in dataset.columns if not col.endswith("_change")]
    default_columns = ["alder_18_34", "alder_35_44", "alder_45_54", "alder_55_64", "alder_65_74", "alder_75_"]
    default_selected = [col for col in default_columns if col in column_choices]
    default_selected = default_selected if default_selected else [column_choices[0]]
    min_year, max_year = int(dataset["year"].min()), int(dataset["year"].max())
else:
    column_choices = []
    default_selected = []
    min_year, max_year = None, None




# p3= ui.card(
#             ui.row(ui.column(6,ui.h6(ui.output_text("compare_title"),style="font-weight: bold;")),
#             ui.column(6,
#                       ui.div( 
#                         ui.div(
#                             ui.input_select("selected_group_1", "Choose variable 1", choices=list(group_to_columns.keys()), selected="Civil tilstand")), 
#                                 ui.output_ui("dynamic_dropdown_2"), style="display: flex; justify-content: flex-end; gap: 12; flex-wrap: wrap;"))),
#             ui.row(ui.output_plot("scatter_plot_2_var")),
#             class_="stat_p3_graf"
#             )


health_councils = sorted(dataset["Sundhedsråd_navn"].dropna().unique())
intervention_year= 2013

def tr(key, lang):
    return translations.get(key, {}).get(lang, key)

app_ui = ui.page_fluid(
    ui.include_css("/Users/zsa/Desktop/Speciale/Dashboard/kode2/css/style.css"),    
    ui.tags.div(
        ui.tags.div(
            ui.tags.div(
                ui.tags.div(
                    ui.h3(ui.output_text("title_text")),
                    class_="header-title"
                ),
                ui.tags.div(
                    ui.input_select("lang", "", {"en": "English", "da": "Dansk"}, selected="da", width="100px")),
                ui.tags.div(
                    ui.input_action_button(
                        id="info_icon",
                        label=None,
                        icon=ui.tags.i(class_="glyphicon glyphicon-info-sign"),
                        class_="navbar-info",
                    ),
                    class_="header-icon" 
                ),
                class_="header-top-row"
            ),
            ui.tags.div(
                ui.output_ui("nav_tabs"),  # Dynamisk menu
                class_="header-tabs"
            ),
            class_="header-bar"
        ),
        class_="header-wrapper"
    ),
    ui.output_ui("tab_content"),
ui.tags.script("""
$(document).on('shiny:value', function(event) {
    const sliderIds = ["year", "year_slider2", "year_range", "data_selected_year"];
    sliderIds.forEach(function(id) {
        setTimeout(function() {
            var el = $("#" + id).data("ionRangeSlider");
            if (el) {
                el.update({
                    prettify_enabled: false
                });
            }
        }, 100); // 100ms delay – juster om nødvendigt
    });
});
"""),
)

info_button_title = ui.input_action_button(
    "info_icon_title", 
    ui.HTML('<span style="display: inline-flex; align-items: center; gap: 8px;">👆<b>MORE INFO</b></span>'),
    style="""
        background-color: #21275A;
        color: #F5F5F7;
        border: none;
        border-radius: 30px;
        padding: 8px 16px;
        font-size: 14;
        cursor: pointer;
        transition: background-color 0.2s ease;
    """,
)



def server(input, output, session):

    @output
    @render.text
    def title_text():
        return t("title", input.lang())

    @output
    @render.ui
    def nav_tabs():
        lang = input.lang()
        return ui.navset_pill(
            ui.nav_panel(t("front_page", lang), value="Front page"),
            ui.nav_panel(t("data", lang), value="Data"),
            ui.nav_panel(t("map", lang), value="Map"),
            ui.nav_panel(t("time_series", lang), value="Time Series – Health Councils"),
            ui.nav_menu(t("statistics", lang),
                ui.nav_panel(t("static_plots", lang), value="Static plots"),
                ui.nav_panel(t("dynamic_plots", lang), value="Dynamic plots"),
            ),
            ui.nav_panel(t("analysis", lang), value="Analysis"),
            ui.nav_panel(t("contact", lang), value="Contact Us"),
            id="main_tabs"
        )

    
    @output
    @render.ui
    def tab_content():
        lang = input.lang()
        selected_tab = input.main_tabs()
        

        if selected_tab == "Front page":
            return ui.layout_columns(
                ui.card(
                    ui.row(
                        ui.column(6,forside_text(input.lang()),ui.output_ui("forside_icon")), 
                        ui.column(6,ui.output_image("logo"), class_="small-logo for_img")), 
                    class_="for_text"),
                )
        
        elif selected_tab == "Data":
            return ui.layout_columns(
                        ui.card(ui.h6(t("Data overview",lang), style="font-weight: bold;"),
                            ui.output_data_frame("data_filtered_table"),
                        class_="data",
                        ),
                    )
        
        elif selected_tab == "Map":
            excluded_variables = ["mand", "year", "Sundhedsråd_navn", "alder_18_34", "alder_35_44", "alder_45_54", "alder_55_64", "alder_65_74", "alder_75_", "opr_land_dk", "opr_land_vest", "opr_land_ikke_vest", "socio_stud",  "Sundhedsråd_kode", "bef", "socio_øvrige", "udd_Grund", "udd_Gym", "udd_Erhverv", "udd_KVU", "udd_MVU", "udd_LVU", "udd_NA", "mr", "ct", "rgt", "DM54", "DM51", "DM48", "DM47", "DM50", "DM_other"]
            filtered_column_choices = {col: dnt(col, lang) for col in column_choices if col not in excluded_variables}

            return ui.layout_columns(
                        ui.card(ui.h6(t("map over the danish health councils",lang), style="font-weight: bold;"), 
                                ui.input_slider("year", t("select Year",lang), min=2007, max=2022, value=2015, step=1), 
                                ui.input_select("variable_to_map", ui.tags.strong(t("Choose variable:",lang)), choices=filtered_column_choices, selected="ryg_pt"),
                                ui.input_checkbox_group("normalize_map", t("Show per 1000 inhabitants",lang), choices={"Yes": ""}, selected=None),
                                class_="kort_slider"
                        ),
                        ui.card(ui.output_ui("map"), height="600px", class_="leaflet-interactive"),
                        col_widths=[3, 9],
                    )
        

        elif selected_tab == "Time Series – Health Councils":
            excluded_variables_time = ["mand", "year", "Sundhedsråd_navn", "Sundhedsråd_kode", "bef"]
            filtered_column_choices_time = {col: dnt(col, lang) for col in column_choices if col not in excluded_variables_time}

            return ui.layout_columns(
                        ui.card(
                            ui.input_checkbox_group(
                            "selectedCouncils", 
                            ui.tags.strong(t("Choose Health Council:",lang)),
                            choices=["Denmark"] + health_councils,
                            selected=["Denmark"],
                            width="100",
                            ),
                            ui.input_checkbox("select_all_councils", t("Select All/None",lang), value=True),
                            class_="time_check"
                        ),
                        ui.card(
                            ui.row(ui.input_select("variable_to_plot", ui.tags.strong(t("Choose variable:",lang)), choices=filtered_column_choices_time, selected="ryg_pt"),
                            ui.input_checkbox_group("normalize_per1000", t("Show per 1000 inhabitants",lang), choices=[""], selected=[])),
                            ui.output_ui("incident_graph"),
                            height="580px",
                            class_="time_graf"
                        ),
                        col_widths=[3, 9],   
                    ),

        elif selected_tab == "Static plots":
            return ui.layout_columns(
                        ui.card(
                            ui.h6(t("Ages of patients over the years (in %)",lang), style="font-weight: bold; margin-bottom: 10;" "text-align: center;"),
                            ui.output_ui("p1"), class_="p1_style"),
                        ui.card(
                            ui.h6(ui.output_text("p2_title"),style="font-weight: bold;""text-align: center;"),
                            ui.row(
                                ui.column(12, ui.input_slider("year_slider2", t("select Year",lang), min=min_year, max=max_year, step=1, ticks=True, value=2010, width="500")    
                                if min_year is not None and max_year is not None else ui.p("no year column found")),
                                ui.column(12, ui.output_ui("p2")),
                            ),
                            class_="p2_style"
                        ),
                        col_widths=[6, 6],
            )
        
        elif selected_tab == "Dynamic plots":
            choices_dict_p3 = {group for group in group_to_columns.keys()}
            choices_p3 = {group: group_translations[group][lang] for group in choices_dict_p3}
            return ui.layout_column_wrap(
                        ui.card(
                            ui.row(ui.column(6,ui.h6(ui.output_text("compare_title"),style="font-weight: bold;")),
                                ui.column(6,
                                    ui.div( 
                                        ui.div(
                                            ui.input_select("selected_group_1", t("Choose variable 1",lang), choices=choices_p3, selected="Marital status")), 
                                            ui.output_ui("dynamic_dropdown_2"), style="display: flex; justify-content: flex-end; gap: 12; flex-wrap: wrap;"))),
                            ui.row(ui.output_plot("scatter_plot_2_var")),
                            class_="stat_p3_graf"
                        ),  
                )
        
        elif selected_tab == "Analysis" :
            excluded_variables = ["mand", "year", "Sundhedsråd_navn", "Sundhedsråd_kode", "bef"]
            filtered_column_choices = {col: dnt(col, lang) for col in column_choices if col not in excluded_variables}



            return ui.div(
                ui.h4(ui.output_ui("dynamic_title"), info_button_title, class_="lyse_h6", style="display: flex; justify-content: center; align-items: center; gap: 10;"), 
                ui.layout_columns(
                    ui.card(
                        ui.row(
                            ui.column(6, ui.input_select("selected_sundhedsråd_lyse", ui.tags.strong(t("Choose Health Council:",lang)), choices=["Denmark"] + list(dataset["Sundhedsråd_navn"].unique()))),
                            ui.column(6, ui.input_select("selected_var", ui.tags.strong(t("Select Variable",lang)), choices=filtered_column_choices, selected="FP"))
                        ),
                        ui.output_ui("baseline_table", style="margin-bottom: 20;"),
                        ui.output_ui("its_table"),
                        class_="baseline-card"
                    ),
                    ui.card(
                        ui.output_ui("its_plot"),
                        style="width: 100;",
                        class_="its-plot-card"
                    ),
                    col_widths=[5, 7],
                    gap="24"
                )
            )
        
        elif selected_tab == "Contact Us":
            return ui.layout_columns(
                        ui.card(
                            kontakt_info(input.lang()),
                            rettigheder(input.lang()), 
                            class_="contact",
                            
                        ), 
                    ),

    @render.ui
    def forside_icon():
        lang = input.lang() 
        return ui.HTML(forside_icon_html(lang))

    output.forside_icon = forside_icon
   

    @render.image
    def logo():
    
        dir = Path(__file__).resolve().parent
        img = {"src": str(dir / "forsidebeskåret.png")} 
        return img

    @render.code
    def selected():
        return input.selected_navset_pill_list()

    
    info_modal()
    @reactive.Effect
    @reactive.event(input.info_icon)
    def _():
        info_modal(input.lang())


    @render.data_frame
    def data_filtered_table():
        lang = input.lang()
        selected_columns = ["year", "Sundhedsråd_navn", "alder_incident", "socio_beskæft", "ryg_pt", "incident", "FP"]


        filtered_dataset_table = dataset[selected_columns]
        renamed_columns = {col: dnt(col, lang) for col in selected_columns}
        renamed_dataset = filtered_dataset_table.rename(columns=renamed_columns)
        
        numeric_cols = renamed_dataset.select_dtypes(include='number').columns
        
        renamed_dataset[numeric_cols] = renamed_dataset[numeric_cols].round(2)

        return render.DataGrid(renamed_dataset)
    
    @reactive.effect
    @reactive.event(input.select_all_councils)
    def toggle_all_councils():
        if input.select_all_councils():
            ui.update_checkbox_group("selectedCouncils", selected=["Denmark"] + health_councils)
        else:
            ui.update_checkbox_group("selectedCouncils", selected=[])
            

    def get_denmark_series(dataset, selected_variable):
    
        denmark_data = (
            dataset
            .groupby("year", as_index=False)[selected_variable]
            .sum()
            .assign(Sundhedsråd_navn="Denmark")
        )
        return denmark_data
    
    @render.ui
    def incident_graph():
        selected_variable = input.variable_to_plot()
        selected_councils = input.selectedCouncils()
        lang = input.lang() 

        req(selected_variable)
        req(selected_councils)

        filtered_health = dataset[dataset["Sundhedsråd_navn"].isin(selected_councils)]
        if "Denmark" in selected_councils:
            denmark_series = get_denmark_series(dataset, selected_variable)
            filtered_health = pd.concat([filtered_health, denmark_series], ignore_index=True)

        if "" in input.normalize_per1000():
            filtered_health[selected_variable] = (
                filtered_health[selected_variable] / filtered_health["bef"] * 1000
            )

        custom_colors = {
                        "Vendsyssel": "#0D47A1", 
                        "Limfjorden": "#64B5F6",  
                        "Kronjylland": "#0097A7", 
                        "Horsens": "#66BB6A",  
                        "Aarhus": "#9E9D24",    
                        "Vestjylland": "#FFB300",
                        "Midt": "#FB8C00",       
                        "Fyn": "#E53935",     
                        "Trekantsområdet": "#F48FB1",  
                        "Sydvestjylland": "#8E24AA",   
                        "Sønderjylland": "#BA68C8",   
                        "Hovedstaden": "#3949AB",     
                        "Hovedstaden Syd og Vest": "#607D8B",  
                        "Hovedstaden Nord": "#00ACC1",       
                        "Nordsjælland": "#00695C",         
                        "Østsjælland og øerne": "#CFD8DC",  
                        "Midt og Vestsjælland": "#212121"   
                }


        display_label = dnt(input.variable_to_plot(), lang)
        display_label_time = dnt(selected_variable, lang)
        display_label_yaxis = dnt_yaxis(selected_variable, lang)
        title_text = f"{display_label} {t('time_title', lang)}"

        fig = px.line(
            filtered_health,
            x="year",
            y=selected_variable,
            color="Sundhedsråd_navn",
            custom_data=[selected_variable],
            color_discrete_map=custom_colors,
            title=f"<b>{title_text}</b>",
            markers=True,
            labels={"year": dnt("year",lang), selected_variable: display_label_yaxis, "Sundhedsråd_navn": t("Health Council",lang)}
            )        
        
        h = t('Health Council', lang)
        year_label = t('year', lang)

        fig.update_traces(
            hovertemplate=(
                f"<b>{h}</b>: %{{fullData.name}}<br>" +  # Bemærk f-string
                f"<b>{year_label}</b>: %{{x}}<br>" +    # Bemærk f-string
                f"<b>{display_label}</b>: " + "%{customdata[0]:.3f}<extra></extra>"
            )
        )

        
        fig.update_layout(
            xaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=False,
                showgrid=False,
                title=t("year",lang)
            ),
            yaxis=dict(
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=False,
                gridcolor="lightgrey",
                griddash="dash",
                showgrid=True
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        html = pio.to_html(fig, config={
            "displaylogo": False,
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["pan2d", "zoomIn2d", "zoomOut2d", "lasso2d", "select2d"],
            "toImageButtonOptions": {
                "filename": "Times_Series_Incident_Plot",
                "format": "png",
                "scale": 2
            }
        }, include_plotlyjs=True, full_html=False)

        return ui.HTML(html)



    def create_folium_map(year, selected_variable_m, normalize=False):
        lang = input.lang()
        filtered_data_map = combined_data[combined_data["year"] == year]


        if normalize:
            if "bef" not in filtered_data_map.columns:
                print("Error in bef column not found")
            else:
                filtered_data_map[selected_variable_m] = (
                    filtered_data_map[selected_variable_m] / filtered_data_map["bef"]
                ) * 1000
                selected_variable_m_label = f"{dnt(selected_variable_m, lang)} per 1000"
        else:
            selected_variable_m_label = dnt(selected_variable_m, lang)

        min_lat, max_lat = 54.2853, 57.9189
        min_lon, max_lon = 7.7768, 15.4417
        m = folium.Map(location=[56.1503, 11.5724], 
                       tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
                        attr='&copy; <a href="https://carto.com/">CARTO</a>',
                       zoom_start=7,
                       zoom_control=False,
                       max_bounds=True,
                       min_zoom=7,
                        min_lat=min_lat,
                        max_lat=max_lat,
                        min_lon=min_lon,
                        max_lon=max_lon,
                        
        )
        
        choropleth_layer = folium.Choropleth(
            geo_data=geo_df,
            data=filtered_data_map,
            columns=["id", selected_variable_m],
            key_on="feature.properties.id",
            fill_color="RdYlBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=(
                f"{'Antal patienter med' if lang == 'da' else 'Amount of patients with'} {selected_variable_m_label} "
                f"{'(relative værdier)' if lang == 'da' else '(relative values)'}"
)
        ).add_to(m)

        popup_data = geo_df.merge(
            filtered_data_map[["id", "Sundhedsråd_navn", selected_variable_m]],
            on="id",
            how="left"
        )

        if selected_variable_m in ['ryg_pt']:
            popup_data[selected_variable_m] = popup_data[selected_variable_m].apply(
                lambda x: str(x).replace(',', '.') if pd.notnull(x) else ''
            )
        elif selected_variable_m in ['dispon_13']:
            popup_data[selected_variable_m] = popup_data[selected_variable_m].apply(
                lambda x: f"{round(x, 2)}".replace(',', '.') 
            )
        else:
            popup_data[selected_variable_m] = popup_data[selected_variable_m].apply(
                lambda x: str(x).replace(',', '.') if pd.notnull(x) else ''
            )
        tooltip_alias = f"{dnt(selected_variable_m, lang)}" + (" per 1000" if normalize else "")
        folium.GeoJson(
            popup_data,
            name="Sundhedsråd",
            style_function=lambda x: {
            "fillColor": "transparent",
            "color": "transparent",
            "weight": 0
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["Sundhedsråd_navn", selected_variable_m],
            aliases=[
                t("Health Council", lang) + ":", 
                tooltip_alias + ":"],
                localize=True,
                sticky=True,
                outline=False,
            ),
            
        ).add_to(m)
        
        return m._repr_html_()
    
    @output
    @render.ui
    def map():
        year = input.year()
        selected_variable_m = input.variable_to_map()
        per_1000_allowed = ["ryg_pt", "FP", "enlig", "samlev", "socio_arbløs", "socio_beskæft", "socio_overførsel", "socio_pension", "incident"]
        normalize_checkbox = "Yes" in input.normalize_map()
        normalize = normalize_checkbox and selected_variable_m in per_1000_allowed

        if normalize_checkbox and selected_variable_m not in per_1000_allowed:
            lang = input.lang()
            ui.notification_show(
                t("normalize_not_allowed", lang),
                type="warning",
                duration=5000
            )
            ui.HTML("""
        <script>
            setTimeout(function() {
                $('.shiny-notification').fadeOut();
            }, 5000);  // Adjust this time in milliseconds
        </script>
        """)
            
        html_map = create_folium_map(year, selected_variable_m, normalize=normalize)

        return ui.HTML(f"""
        <div class="map-container">
            {html_map}
        </div>
    """)

    
    @render.data_frame
    def filtered_data_p1():
        if dataset is None:
            return pd.DataFrame({"Fejl": ["Kunne ikke indlæse datasættet."]})
        selected_cols = input.selected_columns()
        
        if "year" in dataset.columns:
            start_year, end_year = input.year_range()
            df_filtered = dataset[(dataset["year"] >= start_year) & (dataset["year"] <= end_year)]
        else:
            df_filtered = dataset

        if "year" in df_filtered.columns and "year" not in selected_cols:
            selected_cols = ["year"] + selected_cols
        return df_filtered[selected_cols]
    output.filtered_data = filtered_data_p1

    @render.ui
    def p1():
        lang = input.lang()
        if dataset is None or "year" not in dataset.columns:
            return ui.HTML(title="Data not available")

        age_columns = ["alder_18_34", "alder_35_44", "alder_45_54", "alder_55_64", "alder_65_74", "alder_75_"]
        
        labels = ["age_18_34", "age_35_44", "age_45_54", "age_55_64", "age_65_74", "age_75+"]

        for col in age_columns:
            if col not in dataset.columns:
                print(f"Column {col} not found in the dataset.")
                return px.line(title="Missing column")

        df_grouped = dataset.groupby("year")[age_columns].sum().reset_index()

        df_melted = df_grouped.melt(id_vars="year", value_vars= age_columns, var_name="Age Group", value_name="Count")

        label_map = dict(zip(age_columns, [t_age(k, lang) for k in labels]))
        df_melted["Age Group"] = df_melted["Age Group"].map(label_map)

    
        fig = px.area(
            df_melted,
            x = "year",
            y = "Count",
            color = "Age Group",
            groupnorm="percent",
            labels={
            "year": t_age("year", lang),
            "Count": t_age("percentage", lang),
            "Age Group": t_age("age_group", lang),
            },
            color_discrete_sequence= ["#0D47A1", "#1565C0", "#2196F3", "#64B5F6", "#3F51B5", "#7B1FA2"]
        )

        fig.update_layout(
            xaxis=dict(dtick=2, showgrid=False, linecolor="black",),
            yaxis=dict(title=t_age("percentage", lang), ticksuffix="%", linecolor="black", showgrid=True, gridcolor="lightgray", gridwidth=1, griddash="dash"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title_text=t_age("age_group", lang)
            )

        html = pio.to_html(fig, config={
             "displaylogo" : False, 
             "displayModeBar": True,
             "modeBarButtonsToRemove": ["pan2d", "zoomIn2d", "zoomOut2d", "lasso2d", "select2d"],
             "toImageButtonOptions": {
                 "filename": "Age_Distribution_plot_Statestics_Tab",
                 "format": "png",
                 "scale" : 1 
                }
              },
            include_plotlyjs=True, full_html=False)

        return ui.HTML(html) 
       
    output.p1 = p1

 
    @render.ui
    def p2():
        try:
            lang = input.lang()
            if dataset is None or "year" not in dataset.columns:
                return ui.HTML(t("Error in p2 - year column is missing", lang))
        
            sel_year = int(input.year_slider2())
            df_single_year = dataset[dataset["year"] == sel_year].copy()
        
            if "dispon_13" not in df_single_year.columns:
                return ui.HTML(t("Error in dispon_13 column", lang))
        
            custom_bins = [150000, 170000, 190000, 210000, 230000, 250000, 270000, 290000, 310000, 330000, 350000]
            labels = [
                "150-169k", "170-189k", "190-209k", "210-229k", "230-249k","250-269k", "270-289k", "290-309k", "310-329k", "330-349k"]
        
            df_single_year["dispon_cat"] = pd.cut(
                df_single_year["dispon_13"],
                bins=custom_bins,
                labels=labels,
                include_lowest=True,
                right=False
            )
        
            grouped = df_single_year.groupby("dispon_cat", observed=False).size().reindex(labels, fill_value=0)
            df_bar = grouped.reset_index()
            df_bar.columns = [t("Salary Category", lang), t("Number of Patients", lang)]

            fig = px.bar(
                df_bar, 
                x=t("Salary Category", lang),
                y=t("Number of Patients", lang),
                color=t("Salary Category", lang),
                color_discrete_sequence=["#0D47A1", "#1565C0", "#2196F3", "#3F51B5", "#7B1FA2", "#9C27B0", "#C2185B", "#D32F2F", "#F44336", "#FF7043"],
                labels={t("Salary Category", lang): f"{t('Salary Category', lang)} {sel_year}"}

            )
            
            fig.update_layout(
                height=400,
                xaxis = dict(
                    tickangle=-45, 
                    linecolor="black",
                    showgrid=False,
                    showline=True
                ),
                yaxis=dict(
                    gridcolor="lightgray", 
                    tickfont=dict(color="black"), 
                    gridwidth=1,
                    showline=True,
                    linecolor="black",
                    griddash="dash"
                    ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
              )  


            html = pio.to_html(fig, config={
                "displaylogo": False,
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["pan2d", "zoomIn2d", "zoomOut2d", "lasso2d", "select2d"],
                "toImageButtonOptions": {
                    "filename": "Salary_Distribution_plot_Statestics_Tab",
                    "format": "png",
                    "scale": 1
                }
            }, include_plotlyjs=True, full_html=False)

            return ui.HTML(html)
        except Exception as e:
            return ui.HTML(f"<p>Error in p2: {e}</p>")

    output.p2 = p2


    
    @render.text
    def p2_title():
        sel_year_slide = input.year_slider2()
        lang = input.lang()
        if sel_year_slide:
            if lang == "da":
                return f"Lønfordeling for {sel_year_slide}"
            else:
                return f"Salary distribution for {sel_year_slide}"
        else:
            return "Vælg et år" if lang == "da" else "Select a year"
    output.p2_title = p2_title
    
   
    @render.ui
    def dynamic_dropdown_2():
        lang = input.lang()
        selected_1 = input.selected_group_1()
        filtered_choices_dd = [group for group in group_to_columns.keys() if group != selected_1]
        choices = {group: group_translations[group][lang] for group in filtered_choices_dd}
        return ui.input_select(
            "selected_group_2",
            "Choose variable 2" if lang == "en" else "Vælg variabel 2",
            choices=choices,
            selected=filtered_choices_dd[0] if filtered_choices_dd else None,
        )
    output.dynamic_dropdown_2 = dynamic_dropdown_2

    @render.plot
    def scatter_plot_2_var():
        lang = input.lang()
        if dataset is None or "year" not in dataset.columns:
            return plt.figure()

        selected_group_1 = input.selected_group_1()
        selected_group_2 = input.selected_group_2()

        if not selected_group_1 or not selected_group_2:
                return plt.figure()

        if selected_group_1 == selected_group_2:
                fig, ax = plt.subplots()
                ax.text(0.5, 0.5, t("Choose two different variables", lang), ha="center", va="center", fontsize=12)
                ax.axis("off")
                return fig

        variables_1 = group_to_columns.get(selected_group_1)
        variables_2 = group_to_columns.get(selected_group_2)

        if not variables_1 or not variables_2:
                return plt.figure()

        colors_list = ["#0D47A1", 
                        "#2196F3",  
                        "#BBDEFB", 
                        "#7B1FA2", 
                        "plum", 
                        "#C2185B",  
                        "#F0E442",  
                        ]
        
        num_subplots = len(variables_1)
        cols = 4
        rows = (num_subplots + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(50, rows * 4))
        fig.patch.set_facecolor("#F5F5F7")
        axes = axes.flatten()

        all_legend_handles = []
        all_legend_labels = []

        for i, var1 in enumerate(variables_1):
            ax = axes[i]
            ax.set_facecolor("#F5F5F7")

            df_grouped_var1 = (
                dataset[["year", "Sundhedsråd_navn", var1]]
                .dropna()
                .groupby(["year", "Sundhedsråd_navn"])[var1]
                .mean()
                .reset_index()
                .groupby("year")[var1]
                .mean()
                .reset_index()
                )
  
            line = ax.plot(
                    df_grouped_var1["year"],
                    df_grouped_var1[var1],
                    marker="o",
                    linestyle="-",
                    linewidth=2,
                    color = "black",
                    label = t("Chosen variable 1", lang) if t("Chosen variable 1", lang) not in all_legend_labels else None 
                ) [0]

            if "Chosen variable 1" not in all_legend_labels:
                all_legend_handles.append(line)
                all_legend_labels.append(t("Chosen variable 1", lang))

            for j, var2 in enumerate(variables_2):
                if var2 not in dataset.columns:
                    continue

                df_grouped_var2 = (
                    dataset[["year", "Sundhedsråd_navn", var2]]
                    .dropna()
                    .groupby(["year", "Sundhedsråd_navn"])[var2]
                    .mean()
                    .reset_index()
                    .groupby("year")[var2]
                    .mean()
                    .reset_index()
                )

    
                color = colors_list[j % len(colors_list)]
                line = ax.plot(
                    df_grouped_var2["year"],
                    df_grouped_var2[var2],
                    marker="o",
                    linestyle="-",
                    linewidth=2,
                    color=color,
                    label=display_names.get(var2,var2)   
                )[0]

                if dnt(var2, lang) not in all_legend_labels:
                        all_legend_handles.append(line)
                        all_legend_labels.append(dnt(var2, lang))

            tick_years = df_grouped_var2["year"].unique()
            tick_years = tick_years[tick_years % 2 == 0]
            ax.set_xticks(tick_years)
            ax.set_xticklabels(tick_years, rotation=45, ha="right", fontsize=8)
            
            
            wrapped_title = dnt(var1, lang).replace(": ", ":\n") 
            ax.set_title(wrapped_title, fontsize=10)
            ax.set_xlabel(t("year", lang))
            ax.set_ylabel(t("Count of patients in %", lang))
            ax.grid(True, linestyle="--", alpha=0.3)

        for j in range(len(variables_1), len(axes)):
            fig.delaxes(axes[j])

        unique_legend = OrderedDict()
        for handle, label in zip(all_legend_handles, all_legend_labels):
            if label not in unique_legend:
                unique_legend[label] = handle

        fig.legend(
            unique_legend.values(),
            unique_legend.keys(),
            title=t("Chosen variables:",lang),
            loc="lower right",
        )
        plt.subplots_adjust(left=0.1, right=0.98, top=0.92, bottom=0.15, hspace=0.6, wspace=0.3)

        return fig

    output.scatter_plot_2_var = scatter_plot_2_var

    @render.text
    def compare_title():
        lang = input.lang()
        group1 = input.selected_group_1()
        group2 = input.selected_group_2()

        if group1 and group2 and group1 != group2:
            return f"{t('Compare', lang)}: {gt(group1, lang)} {t('and', lang)} {gt(group2, lang)}"
        elif group1 == group2:
            return t("Choose two different variables", lang)
        else:
            return ""
    output.compare_title = compare_title


    @reactive.calc

    def selected_data_lyse():
        selected_råd = input.selected_sundhedsråd_lyse()
        selected_var = input.selected_var()

        if selected_råd == "Denmark":
            df_lyse = (
                dataset
                .groupby("year", as_index=False)[selected_var]
                .mean()
            )
            df_lyse["Sundhedsråd_navn"] = "Denmark"
        else:
            df_lyse = dataset[dataset["Sundhedsråd_navn"] == selected_råd].copy()

        df_lyse["time"] = df_lyse["year"] - 2007

        intervention_point = intervention_year - 2007

        df_lyse["time_before_intervention"] = df_lyse["time"].apply(
            lambda x: x if x < intervention_point else 0
        )

        df_lyse["time_after_intervention"] = df_lyse["time"].apply(
            lambda x: x - intervention_point if x >= intervention_point else 0
        )

        df_lyse["intervention"] = (df_lyse["year"] >= intervention_year).astype(int)

        return df_lyse, selected_var
    
    @reactive.calc
    def its_model():
        df_lyse, selected_var = selected_data_lyse()
        X = sm.add_constant(df_lyse[["time_before_intervention", "intervention", "time_after_intervention"]])
        model = sm.OLS(df_lyse[selected_var], X).fit()
        return model
    
    @output
    @render.table
    def baseline_table():
        lang = input.lang()
        df, selected_var = selected_data_lyse()

        pre_intervention = df[df["year"] < intervention_year]
        post_intervention = df[df["year"] >= intervention_year]

        baseline_data = {
            t("Period",lang): [t("Before Intervention",lang), t("After Intervention", lang)],
            t("Mean Rate",lang): [
                pre_intervention[selected_var].mean(),
                post_intervention[selected_var].mean()
            ],
            "Standard Deviation": [
                pre_intervention[selected_var].std(),
                post_intervention[selected_var].std()
            ],
            t("Number of Observations",lang): [
                len(pre_intervention),
                len(post_intervention)
            ]
        }
        
        baseline_df = pd.DataFrame(baseline_data)
        baseline_df = baseline_df.round(3)
        return baseline_df

    @output
    @render.table
    def its_table():
        lang = input.lang()

        model = its_model()
        df, selected_var = selected_data_lyse()

        params = model.params
        bse = model.bse
        pvals = model.pvalues
        r2 = model.rsquared
        n = int(model.nobs)

        pre_intervention = df[df["year"] < intervention_year]
        post_intervention = df[df["year"] >= intervention_year]

        baseline_mean = pre_intervention[selected_var].mean()
        X = sm.add_constant(df[["time_before_intervention", "intervention", "time_after_intervention"]])
        df["predicted"] = model.predict(X)
        post_mean = df.loc[df["intervention"] == 1, "predicted"].mean()

        relative_effect = (post_mean - baseline_mean) / baseline_mean


        results = pd.DataFrame({
            "Coefficient": [
                f"{params['time_before_intervention']:.3f} ({bse['time_before_intervention']:.3f})",
                f"{params['intervention']:.3f} ({bse['intervention']:.3f})",
                f"{params['time_after_intervention']:.3f} ({bse['time_after_intervention']:.3f})",
                f"{params['const']:.3f} ({bse['const']:.3f})",
            ],
            "p-value": [
                f"{pvals['time_before_intervention']:.3f}",
                f"{pvals['intervention']:.3f}",
                f"{pvals['time_after_intervention']:.3f}",
                f"{pvals['const']:.3f}",
            ]
        }, index=[t("Trend Before",lang), t("Level Change (at Intervention)",lang), t("Trend After",lang), t("Constant",lang)])

    
        r2_row = pd.DataFrame({"Coefficient": [f"{r2:.3f}"], "p-value": [""]}, index=["R-squared"])
        n_row = pd.DataFrame({"Coefficient": [f"{n}"], "p-value": [""]}, index=["Observations"])

        rel_eff_row = pd.DataFrame({"Coefficient": [f"{relative_effect:.3f}"], "p-value": [""]}, index=["Relative Effect"])

        final_table = pd.concat([results, r2_row, n_row, rel_eff_row]).reset_index()
        final_table.columns.name = None  
        final_table = final_table.rename(columns={"index": "Variable"})
        return final_table

    @output
    @render.ui
    def its_plot():

        lang= input.lang()
        
        req(input.selected_sundhedsråd_lyse())
        req(input.selected_var())
        model = its_model()
        df, selected_var = selected_data_lyse()          

        X = sm.add_constant(df[["time_before_intervention", "intervention", "time_after_intervention"]], has_constant='add')
        df["predicted"] = model.predict(X)

        pre = df[df["year"] < intervention_year]
        post = df[df["year"] >= intervention_year]

        display_label_yaxis = display_names_yaxis_translated.get(selected_var, {}).get(lang, selected_var)


        fig = px.scatter(
            df, 
            x="year",
            y=selected_var,
            opacity=0.7,
            labels={"year": display_name_translated["year"][lang], selected_var: display_label_yaxis}
        )

        fig.add_scatter(
            x=pre["year"],
            y = pre["predicted"],
            mode = "lines",
            name= display_name_translated.get("Fitted Pre-Intervention", {}).get(lang, "Fitted Pre-Intervention"), 
            line=dict(color="blue", width=2)
        )

        fig.add_scatter(
            x=[None],
            y=[None],
            mode="lines",
            name= display_name_translated.get("Intervention Year", {}).get(lang, "Intervention Year"), 
            line=dict(color="black", dash="dash")
                )


        fig.add_scatter(
            x=post["year"],
            y = post["predicted"],
            line_dash="dash",
            name= display_name_translated.get("Fitted Post-Intervention", {}).get(lang, "Fitted Post-Intervention"), 
            line=dict(color="red", width=2)
        )

        fig.add_vline(
            x=intervention_year,
            line_dash="dash",
            line_color="black",
        )

        fig.update_layout(
                xaxis = dict(
                    tickmode="array",
                    tickvals=[y for y in sorted(df["year"].unique()) if y % 2 == 0],
                    showline=True,
                    linecolor="black",
                    showgrid=False,
                ),
                yaxis=dict(
                    gridcolor="lightgray", 
                    tickfont=dict(color="black"), 
                    gridwidth=1,
                    showline=True,
                    linecolor="black",
                    griddash="dash"
                    ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t = 20, b=50, l=50, r=20)
              )  
        
        fig.update_traces(marker=dict(color="black"), selector=dict(mode="markers"))

        html = pio.to_html(fig, config={
            "displaylogo": False,
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["pan2d", "zoomIn2d", "zoomOut2d", "lasso2d", "select2d"],
            "toImageButtonOptions": {
                "filename": "ITS_Plot",
                "format": "png",
                "scale": 2
            }
        }, include_plotlyjs=True, full_html=False)

        return ui.HTML(html)
    

    @render.ui
    def dynamic_title():

        lang = input.lang()

        selected_var = input.selected_var()
        råd = input.selected_sundhedsråd_lyse()

        var_name = display_name_translated.get(selected_var, {}).get(lang, selected_var)
        title_html = f"<b>{texts['its_title'][lang]}:</b> {var_name} {texts['in'][lang]} {råd}"
        return ui.HTML(title_html)


    @reactive.Effect
    @reactive.event(input.info_icon_title)
    def _():
        info_modal_title(input.lang())

   
    
app = App(app_ui, server)





