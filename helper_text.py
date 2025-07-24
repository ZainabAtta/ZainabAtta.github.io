from shiny.ui import modal_show, modal, modal_button
from htmltools import TagList, tags
from shiny import ui

translations = {
    "forside_intro": {
        "en": "Welcome to the dashboard. Here you can explore and analyze spine data for Danish health councils.",
        "da": "Velkommen til dashboardet. Her kan du udforske og analysere rygdata for danske sundhedsråd."
    },
    "dataset_information_title": {
        "en": "Dataset Information",
        "da": "Datasætinformation"
    },
    "dataset_information_body": {
        "en": """For the app, we have chosen data from SPINEDATA:SDU and Statistic Denmark.
We had help aggregating the data for this app.""",
        "da": """Til appen har vi valgt data fra SPINEDATA:SDU og Danmarks Statistik.
Vi fik hjælp til at sammenstille dataene til denne app."""
    },
    "spinedata_link": {
        "en": "SPINEDATA:SDU",
        "da": "SPINEDATA:SDU"
    },
    "spinedata_link_url": {
        "en": "https://www.sdu.dk/en/forskning/dache/forskning/rygdata",
        "da": "https://www.sdu.dk/da/forskning/dache/forskning/rygdata"
    },
    "første_tekst_title": {
        "en": "Design and development of a dashboard for spine data",
        "da": "Design og udvikling af et dashboard for rygdata"
    },
    "første_tekst_body": {
        "en": """This app provides a visual overview of spine data based on the 17 health councils in Denmark, 
covering the years 2007 to 2022.""",
        "da": """Denne app giver et visuelt overblik over rygdata baseret på de 17 sundhedsråd i Danmark, 
og dækker årene 2007 til 2022."""
    },
    "problem_statement_title": {
        "en": "Why a dashboard",
        "da": "Hvorfor et dashboard"
    },
    "problem_statement_body": {
        "en": """In an increasingly data-driven world, the need to interpret and communicate complex data is essential for informed 
decision-making within research, healthcare and policy.
To understand how back pain diagnosis impacts patients and health care facilities, we have used the variables: Age, Health Councils,
Diagnostic tool, Main diagnosis, Education level, Labour-market participant, Country of origin.
We have visualized if there has been an impact of the 2013 law reform.""",
        "da": """I en stadigt mere datadrevet verden er behovet for at fortolke og kommunikere komplekse data essentielt for informerede beslutninger indenfor forskning, sundhedspleje og politik.
For at forstå, hvordan rygdiagnoser påvirker patienter og sundhedsvæsen, har vi brugt variablerne: Alder, Sundhedsråd, Diagnostisk værktøj, Hoveddiagnose, Uddannelsesniveau, Arbejdsmarkedstilknytning, Oprindelsesland.
Vi har visualiseret, om der har været en effekt af lovændringen i 2013."""
    },
    "forside_heading": {
        "en": "Welcome to the spine data app!",
        "da": "Velkommen til rygdata-appen!"
    },
    "forside_intro": {
        "en": """
            The SPINEDATA project at the University of Southern Denmark (SDU) 
            is a research initiative under the Danish Centre for Health Economics (DaCHE). 
            It focuses on the collection and analysis of data related to spine disorders, 
            aiming to enhance understanding of their causes, treatment outcomes, and economic implications. 
            The project utilizes comprehensive Danish health registries to conduct longitudinal studies, 
            providing insights that inform healthcare policy and practice. 
            A multidisciplinary coordinator group oversees the project, 
            ensuring a collaborative approach to addressing the complexities of spine-related health issues.
        """,
        "da": """
            SPINEDATA-projektet ved Syddansk Universitet (SDU) 
            er et forskningsinitiativ under Dansk Center for Sundhedsøkonomi (DaCHE).
            Projektet fokuserer på indsamling og analyse af data om rygsygdomme
            for at øge forståelsen af årsager, behandlingsresultater og de økonomiske konsekvenser.
            Projektet benytter omfattende danske sundhedsregistre til at udføre longitudinelle studier,
            som giver indsigter, der kan informere sundhedspolitik og praksis.
            En tværfaglig koordinatorgruppe leder projektet og sikrer et samarbejdende fokus på de komplekse rygrelaterede sundhedsproblemer.
        """
    },
    "contact_title": {
        "en": "For further information, contact us",
        "da": "For yderligere information, kontakt os"
    },
    "contact_dev_subtitle": {
        "en": "For further information, contact the developer/students:",
        "da": "Kontakt udviklerne/studerende:"
    },
    "contact_supervisor_subtitle": {
        "en": "For further information, contact the supervisor:",
        "da": "Kontakt vejleder:"
    },
    "rettigheder": {
        "en": (
            "© 2025 Sandra Boss & Zainab Sattar Atta – All rights reserved. "
            "This dashboard was developed as part of a master's thesis at the University of Southern Denmark. "
            "Reproduction or redistribution without explicit permission is prohibited. "
            "Department of Mathematics and Computer Science, SDU."
        ),
        "da": (
            "© 2025 Sandra Boss & Zainab Sattar Atta – Alle rettigheder forbeholdes. "
            "Dette dashboard er udviklet som led i et speciale på Syddansk Universitet. "
            "Kopiering eller videreformidling uden udtrykkelig tilladelse er forbudt. "
            "Institut for Matematik og Datalogi, SDU."
        ),
    },
    "ITS_heading": {
        "en": "What is an Interrupted Time Series (ITS) analysis?",
        "da": "Hvad er en Interrupted Time Series (ITS) analyse?"
    },
    "ITS_body": {
        "en": """
            An ITS analysis looks at trends over time before and after a specific event or intervention 
            — like a new law or health policy. it explains if the intervention had an effect, 
            how big the effect was, and if the effect was significant. It’s especially useful when a randomized experiment is not possible.
        """,
        "da": """
            En ITS-analyse ser på tendenser over tid før og efter en specifik begivenhed eller intervention
            – fx en ny lov eller sundhedspolitik. Analysen viser, om interventionen havde en effekt,
            hvor stor effekten var, og om den var signifikant. Det er særligt nyttigt, når et randomiseret forsøg ikke er muligt.
        """
    },
    "reform_heading": {
        "en": "Policy Reform as the Intervention",
        "da": "Reform som intervention"
    },
    "reform_body": {
        "en": """
            In this case, the ITS analysis examines trends before and after a major Danish law reform on 
            early retirement (førtidspension) introduced in 2013. 
            The reform aimed to reduce the number of new early retirement cases by encouraging 
            employment and rehabilitation instead. By comparing data from before and after the reform, 
            the analysis helps us assess whether the policy had a statistically significant impact.
        """,
        "da": """
            I dette tilfælde undersøger ITS-analysen tendenser før og efter en større dansk lovreform om 
            førtidspension, der blev indført i 2013.
            Reformen havde til formål at reducere antallet af nye førtidspensioner gennem fokus på beskæftigelse og rehabilitering.
            Ved at sammenligne data fra før og efter reformen kan analysen vurdere, om ændringen har haft en statistisk signifikant effekt.
        """
    },

}
def tr(key, lang):
    return translations.get(key, {}).get(lang, "")

forside_icon_text = {
    "title1": {"da": "Data indsigt", "en": "Reveal insights"},
    "desc1": {"da": "Opdag tendenser og mønstre<br>i rygdata.", "en": "Detect trends and patterns<br>in spine data."},
    "title2": {"da": "Fremhæv udviklinger", "en": "Highlight developments"},
    "desc2": {"da": "Følg behandlinger, resultater<br>og ændringer over tid.", "en": "Track treatments, outcomes,<br>and changes over time."},
    "title3": {"da": "Understøt analyser", "en": "Support analysis"},
    "desc3": {"da": "Giv intuitive visualiseringer<br>til at udforske komplekse data.", "en": "Provide intuitive visualizations<br>to explore complex data."}
}
def fit(key, lang):
    return forside_icon_text.get(key, {}).get(lang, "")
def forside_icon_html(lang):
    return f"""
        <div style="display: flex; flext-wrap: nowrap; justify-content: center; gap: 32px; margin-top: 32px; overflow-x:auto;">
            <div style="flex: 1; min-width: 200px; max-width: 250px; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="font-size: 3vw; margin-bottom: 1vw;">🔍</div>
                <strong style="margin-bottom: 0.5px; font-size: 1.2vw">{fit('title1', lang)}</strong>
                <p style="margin: 0;">{fit('desc1', lang)}</p>
            </div>
            <div style="flex: 1; min-width: 200px; max-width:250px; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="font-size: 3vw; margin-bottom: 1vw;">📊</div>
                <strong style="margin-bottom: 0.5px; font-size: 1vw">{fit('title2', lang)}</strong>
                <p style="margin: 0;">{fit('desc2', lang)}</p>
            </div>
            <div style="flex: 1; min-width: 200px; max-width: 250px; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="font-size: 3vw; margin-bottom: 1vw;">🗂️</div>
                <strong style="margin-bottom: 0.5px; font-size:1.2vw">{fit('title3', lang)}</strong>
                <p style="margin: 0;">{fit('desc3', lang)}</p>
            </div>
        </div>
    """
texts = {
    "title": {
        "en": "Design and development of a dashboard for spine data",
        "da": "Design og udvikling af et dashboard til ryg data"
    },
    "front_page": {"en": "Front page", "da": "Forside"},
    "data": {"en": "Data", "da": "Data"},
    "map": {"en": "Map", "da": "Kort"},
    "time_series": {"en": "Time Series – Health Councils", "da": "Tidsserier – Sundhedsråd"},
    "statistics": {"en": "Statistics", "da": "Statistik"},
    "static_plots": {"en": "Static plots", "da": "Statiske grafer"},
    "dynamic_plots": {"en": "Dynamic plots", "da": "Dynamiske grafer"},
    "analysis": {"en": "Analysis", "da": "Analyse"},
    "contact": {"en": "Contact Us", "da": "Kontakt os"},
    "Data overview": {"en":" Data overview", "da": "Dataoversigt"},
    "map over the danish health councils": {"en": "Map over the Danish health councils", "da": "Kort over de danske sundhedsråd"},
    "select Year": {"en": "Choose a Year", "da": "Vælg et år"},
    "Choose variable:": {"en": "Choose variable:", "da": "Vælg variabel:"},
    "Show per 1000 inhabitants": {"en": "Show per 1000 inhabitants", "da": "Vis pr. 1000 indbyggere"},
    "Choose Health Council:": {"en": "Choose Health Council", "da": "Vælg Sundhedsråd"},
    "Denmark": {"en": "Denmark", "da": "Danmark"},
    "Select All/None": {"en": "Select All/None", "da": "Vælg alle/ingen"},
    "Ages of patients over the years (in %)": {"en": "Ages of patients over the years (in %)", "da": "Patienters alder over årene (i %)"},
    "Select Variable": {"en": "Select a Variable", "da": "Vælg en Variabel"},
    "time_title": {"en": "over the years for selected health councils", "da": "over årene for valgte sundhedsråd"},
    "Health Council": {"en": "Health Council", "da": "Sundhedsråd"},
    "year": {"en": "Year", "da": "År"},
    "normalize_not_allowed": {"en": "This variable cannot be displayed per 1000 inhabitants. The selected variable is displayed as originally.",
        "da": "Denne variabel kan ikke vises pr. 1000 indbyggere. Den valgte variabel vises som oprindeligt."},
    "Salary Category": {"en": "Salary Category","da": "Lønkategori"},
    "Number of Patients": {"da": "Antal patienter", "en": "Number of Patients"},
    "Error in p2 - year column is missing": {"da": "Fejl i p2 – 'year'-kolonnen mangler", "en": "Error in p2 - year column is missing"},
    "Error in dispon_13 column": {"da": "Fejl – 'dispon_13'-kolonnen mangler", "en": "Error in dispon_13 column"},
    "Error in p2:": {"da": "Fejl i p2:", "en": "Error in p2:"},
    "Count of patients in %": {"da": "Antal patienter i %", "en": "Count of patients in %"},
    "Chosen variables:": {"da": "Valgte variable:", "en": "Chosen variables:"},
    "Choose two different variables": {"da": "Vælg to forskellige variable", "en": "Choose two different variables"},
    "Count of patients in %": {"da": "Antal patienter i %", "en": "Count of patients in %"},
    "Chosen variable 1": {"da": "Valgt variabel 1", "en": "Chosen variable 1"},
    "Chosen variables:": {"da": "Valgte variable:", "en": "Chosen variables:"},
    "Compare": {"da": "Sammenlign", "en": "Compare"},
    "and": {"da": "og", "en": "and"},
    "Choose variable 1": {"da": "Vælg variabel 1", "en": "Choose variable 1"},
    "Period": {"da": "Periode", "en": "Period"},
    "Before Intervention": {"da": "Før intervention", "en": "Before Intervention"},
    "After Intervention": {"da": "Efter intervention", "en": "After Intervention"},
    "Mean Rate": {"da": "Gennemsnit rate", "en": "Mean Rate"},
    "Number of Observations": {"da": "Antal observationer", "en": "Number of Observations"},
    "Coefficient": {"da": "Koeficient", "en": "Coefficient"},
    "Trend Before": {"da": "Trend før", "en": "Trend Before"},
    "Level Change (at Intervention)": {"da": "Niveauændring (ved intervention)", "en": "Level Change (at Intervention)"},
    "Trend After": {"da": "Trend efter", "en": "Trend After"},
    "Constant": {"da": "Konstant", "en": "Constant"},
    "Relative Effect": {"da": "Relativ effekt", "en": "Relative Effect"},
    "Observations": {"da": "Observationer", "en": "Observations"},
    "Variable": {"da": "Variabel", "en": "Variable"},
    "Coefficient_table": {"da": "Koeficient", "en": "Coefficient"},
    "its_title": {"da": "Interrupted Time Series", "en": "Interrupted Time Series"},
    "in": {"da": "i", "en": "in"},
    #"Early Retirement": {"da": "Førtidspens", "en": "Early Retirement"},


}

def t(key, lang):
    return texts.get(key, {}).get(lang, key)

age_plot_labels = {
    "age_18_34": {"da": "Alder 18-34", "en": "Age 18-34"},
    "age_35_44": {"da": "Alder 35-44", "en": "Age 35-44"},
    "age_45_54": {"da": "Alder 45-54", "en": "Age 45-54"},
    "age_55_64": {"da": "Alder 55-64", "en": "Age 55-64"},
    "age_65_74": {"da": "Alder 65-74", "en": "Age 65-74"},
    "age_75+": {"da": "Alder 75+", "en": "Age 75+"},
    "year": {"da": "År", "en": "Year"},
    "percentage": {"da": "Procent", "en": "Percentage"},
    "age_group": {"da": "Aldersgrupper", "en": "Age Groups"},
}

def t_age(key, lang):
    return age_plot_labels.get(key, {}).get(lang, key)

def dataset_information(lang):
    return TagList(
        tags.strong(tags.h3(tr("dataset_information_title", lang))),
        tags.p(
            tr("dataset_information_body", lang),
            style="""
            text-align: justify;
            word-break:break-word;
            hyphens: auto;
            """,
        ),
        tags.ul(
            tags.li(
                tags.a(
                    tr("spinedata_link", lang),
                    href=tr("spinedata_link_url", lang),
                )
            ),
        ),
    )
def første_tekst(lang):
    return TagList(
        tags.strong(tags.h3(tr("første_tekst_title", lang))),
        tags.p(
            tr("første_tekst_body", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
    )
def problem_statement(lang):
    return TagList(
        tags.strong(tags.h3(tr("problem_statement_title", lang))),
        tags.p(
            tr("problem_statement_body", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
    )
def info_modal(lang="en"):
    modal_show(
        modal(
            første_tekst(lang),
            tags.hr(),
            problem_statement(lang),
            tags.hr(),
            dataset_information(lang),
            size="l",
            easy_close=True,
            footer=modal_button("Close"),
        )
    )


def forside_text(lang):
    return tags.div(
        tags.h5(tr("forside_heading", lang), style="font-weight: bold;"),
        tags.p(
            tr("forside_intro", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
        tags.h5(tr("forside_purpose_heading", lang), style="font-weight: bold;"),
        tags.p(
            tr("forside_purpose_text", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
    )

def kontakt_info(lang):
    return tags.div(
        tags.h3(tr("contact_title", lang), style="font-weight: bold;"),
        tags.h6(tr("contact_dev_subtitle", lang), style="font-weight: bold;"),
        tags.p("zasat23@student.sdu.dk"),
        tags.p("sboss23@student.sdu.dk"),
        tags.h6(tr("contact_supervisor_subtitle", lang), style="font-weight: bold;"),
        tags.ul(
            tags.li(
                tags.a(
                    "Kim Rose Olsen",
                    href="https://portal.findresearcher.sdu.dk/da/persons/krolsen"
                ),
            ),
        ),
        tags.ul(
            tags.li(
                tags.a(
                    "Nicolai Damslund",
                    href="https://portal.findresearcher.sdu.dk/da/persons/nicolai-damslund"
                ),
            ),
        ),
        tags.ul(
            tags.li(
                tags.a(
                    "Christian Skovsgaard",
                    href="https://portal.findresearcher.sdu.dk/da/persons/chsko"
                ),
            ),
        ),
    )

def rettigheder(lang):
    return tags.footer(
        tags.p(
            tr("rettigheder", lang),
            style="""
                font-size: 0.75rem;
                color: #888;
                text-align: center;
                margin-top: 2em;
                padding: 1em 0;
            """
        ),
        style="""
            width: 100%;
            position: relative;
            bottom: 0;
        """
    )

def ITS(lang):
    return TagList(
        tags.strong(tags.h5(tr("ITS_heading", lang), style="font-weight: bold;")),
        tags.p(
            tr("ITS_body", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
    )

def Reform(lang):
    return TagList(
        tags.strong(tags.h5(tr("reform_heading", lang), style="font-weight: bold;")),
        tags.p(
            tr("reform_body", lang),
            style="""
                text-align: justify;
                word-break:break-word;
                hyphens: auto;
            """,
        ),
    )
def info_modal_title(lang):
    modal_show(
        modal(
            ITS(lang),
            tags.hr(),
            Reform(lang),
            tags.hr(),
            size="l",
            easy_close=True,
            footer=modal_button("Close"),
        )
    )
    

group_to_columns = {
        "Marital status": ["enlig", "samlev"],
        "Country of origin": ["opr_land_dk", "opr_land_ikke_vest", "opr_land_vest"],
        "Labour-market participant" : [ "socio_beskæft", "socio_stud", "socio_arbløs", "socio_overførsel", "socio_øvrige" ],
        "Education level": ["udd_Grund", "udd_Gym", "udd_Erhverv", "udd_KVU", "udd_MVU", "udd_LVU", "udd_NA"],
        "Diagnostic tool" : ["mr", "rgt", "ct"],
        "Main diagnosis" : ["DM54", "DM51", "DM47", "DM48", "DM50", "DM_other"],

}
group_translations = {
    "Marital status": {"en": "Marital status", "da": "Civil tilstand"},
    "Country of origin": {"en": "Country of origin", "da": "Oprindelsesland"},
    "Labour-market participant": {"en": "Labour-market participant", "da": "Arbejdsmarkedstilknytning"},
    "Education level": {"en": "Education level", "da": "Uddannelsesniveau"},
    "Diagnostic tool": {"en": "Diagnostic tool", "da": "Diagnostisk værktøj"},
    "Main diagnosis": {"en": "Main diagnosis", "da": "Hoveddiagnose"},
}

def gt(key, lang):
    return group_translations.get(key, {}).get(lang, key)

display_names = {
    "enlig" : "Single",
    "Civil tilstand" : "Marital status",
    "samlev" : "Cohabiting",
    "opr_land_dk" : "Country of origin: Denmark",
    "opr_land_vest" : "Country of origin: Western",
    "opr_land_ikke_vest" : "Country of origin: Non-Western",
    "socio_beskæft" : "Self-employed, employed or student",
    "socio_arbløs" : "Unemployed", 
    "socio_overførsel" : "Receiving public help",
    "socio_pension" : "Retired or on early retirement",
    "socio_stud" : "Student",
    "socio_øvrige" : "Other employment status",
    "udd_Grund" : "Highest completed education: Primary school",
    "udd_Gym" :  "Highest completed education: High school",
    "udd_Erhverv" : "Highest completed education: Vocational education",
    "udd_Videregående" : "Highest completed education: Bachelor's. Master's or PhD", 
    "udd_KVU" :  "Shorter tertiary degree",
    "udd_MVU" : "Medium tertiary degree",
    "udd_LVU" : "Longer tertiary degree",
    "udd_NA" :  "Unknown edducation level",
    "DM54": "Dorsalgia",
    "DM51": "Thoracic and lumbar disc disorders",
    "DM47": "Spondylosis", 
    "DM48": "Other spondylopathies",
    "DM50": "Cervical disc disorders",
    "DM_other": "Other Diagnoses",
    "ryg_pt" : "Patients with Spine problems",
    "Aktions diagnose" : "Main diagnosis",
    "rgt" : "X-ray",
    "mr" : "MR scan",
    "ct" : "CT scan",
    "type af behandling" : "Treatment type",
    "FP" : "Early Retirement - (førtidspension)",
    "Sundhedsråd_kode" : "Health Council code",
    "alder_incident" : "Incident age",
    "alder_18_34" : "Patients Aged from 18 to 34",
    "alder_35_44" : "Patients Aged from 35 to 44",
    "alder_45_54" : "Patients Aged from 45 to 54",
    "alder_55_64" : "Patients Aged from 55 to 64",
    "alder_65_74" : "Patients Aged from 65 to 74",
    "alder_75_" : "Patients Aged from 75 and up",
    "dispon_13" : "Salary",
    "Sundhedsråd_navn" : "Health Counsil",
    "bef" : "Population size",
    "incident" : "Incident",

}

display_name_translated = {
    "year": {"da": "År", "en": "Year"},
    "enlig": {"da": "Enlig", "en": "Single"},
    "Civil tilstand": {"da": "Civilstand", "en": "Marital status"},
    "samlev": {"da": "Samlevende", "en": "Cohabiting"},
    "opr_land_dk": {"da": "Oprindelsesland: Danmark", "en": "Country of origin: Denmark"},
    "opr_land_vest": {"da": "Oprindelsesland: Vestlige lande", "en": "Country of origin: Western"},
    "opr_land_ikke_vest": {"da": "Oprindelsesland: Ikke-vestlige lande", "en": "Country of origin: Non-Western"},
    "socio_beskæft": {"da": "Selvstændig, ansat eller studerende", "en": "Self-employed, employed or student"},
    "socio_arbløs": {"da": "Arbejdsløs", "en": "Unemployed"},
    "socio_overførsel": {"da": "Modtager offentlig hjælp", "en": "Receiving public help"},
    "socio_pension": {"da": "Pensionist eller førtidspensionist", "en": "Retired or on early retirement"},
    "socio_stud": {"da": "Studerende", "en": "Student"},
    "socio_øvrige": {"da": "Anden beskæftigelse", "en": "Other employment status"},
    "udd_Grund": {"da": "Højest fuldførte uddannelse: Grundskole", "en": "Highest completed education: Primary school"},
    "udd_Gym": {"da": "Højest fuldførte uddannelse: Gymnasial", "en": "Highest completed education: High school"},
    "udd_Erhverv": {"da": "Højest fuldførte uddannelse: Erhvervsuddannelse", "en": "Highest completed education: Vocational education"},
    "udd_Videregående": {"da": "Højest fuldførte uddannelse: Videregående", "en": "Highest completed education: Bachelor's, Master's or PhD"},
    "udd_KVU": {"da": "Kort videregående uddannelse", "en": "Shorter tertiary degree"},
    "udd_MVU": {"da": "Mellemlang videregående uddannelse", "en": "Medium tertiary degree"},
    "udd_LVU": {"da": "Lang videregående uddannelse", "en": "Longer tertiary degree"},
    "udd_NA": {"da": "Ukendt uddannelsesniveau", "en": "Unknown education level"},
    "DM54": {"da": "Dorsalgi", "en": "Dorsalgia"},
    "DM51": {"da": "Thorakal og lumbal diskusprolaps", "en": "Thoracic and lumbar disc disorders"},
    "DM47": {"da": "Spondylose", "en": "Spondylosis"},
    "DM48": {"da": "Andre spondylopatier", "en": "Other spondylopathies"},
    "DM50": {"da": "Cervikal diskusprolaps", "en": "Cervical disc disorders"},
    "DM_other": {"da": "Andre diagnoser", "en": "Other Diagnoses"},
    "ryg_pt": {"da": "Rygpatienter", "en": "Patients with Spine problems"},
    "Aktions diagnose": {"da": "Aktionsdiagnose", "en": "Main diagnosis"},
    "rgt": {"da": "Røntgen", "en": "X-ray"},
    "mr": {"da": "MR-scanning", "en": "MR scan"},
    "ct": {"da": "CT-scanning", "en": "CT scan"},
    "type af behandling": {"da": "Behandlingstype", "en": "Treatment type"},
    "FP": {"da": "Førtidspension", "en": "Early Retirement - (førtidspension)"},
    "Sundhedsråd_kode": {"da": "Sundhedsråd kode", "en": "Health Council code"},
    "alder_incident": {"da": "Alder ved incident", "en": "Incident age"},
    "alder_18_34": {"da": "Patienter i alderen 18 til 34", "en": "Patients aged from 18 to 34"},
    "alder_35_44": {"da": "Patienter i alderen 35 til 44", "en": "Patients aged from 35 to 44"},
    "alder_45_54": {"da": "Patienter i alderen 45 til 54", "en": "Patients aged from 45 to 54"},
    "alder_55_64": {"da": "Patienter i alderen 55 til 64", "en": "Patients aged from 55 to 64"},
    "alder_65_74": {"da": "Patienter i alderen 65 til 74", "en": "Patients aged from 65 to 74"},
    "alder_75_": {"da": "Patienter i alderen 75 og opefter", "en": "Patients aged from 75 and up"},
    "dispon_13": {"da": "Lønindkomst", "en": "Salary"},
    "Sundhedsråd_navn": {"da": "Sundhedsråd navn", "en": "Health Council"},
    "bef": {"da": "Befolkningstal", "en": "Population size"},
    "incident": {"da": "Incident", "en": "Incident"},
    "Fitted Pre-Intervention": {"da": "Fitted før intervention", "en": "Fitted Pre-Intervention"},
    "Fitted Post-Intervention": { "da": "Fitted efter intervention", "en": "Fitted Post-Intervention"},
    "Intervention Year": { "da": "Interventionsår", "en": "Intervention Year"},
    "year": {"da": "År", "en": "Year"}

}
def dnt(key, lang):
    return display_name_translated.get(key, {}).get(lang, key)

display_names_yaxis = {
    "enlig" : "Single [% of spine cases]",
    "Civil tilstand" : "Material status [% of spine cases]",
    "samlev" : "Cohabiting [% of spine cases]",
    "opr_land_dk" : "Country of origin: Denmark [% of spine cases]",
    "opr_land_vest" : "Country of origin: Western [% of spine cases]",
    "opr_land_ikke_vest" : "Country of origin: Non-Western [% of spine cases]",
    "socio_beskæft" : "Self-employed, employed or student [% of spine cases]",
    "socio_arbløs" : "Unemployed [% of spine cases]", 
    "socio_overførsel" : "Receiving public help [% of spine cases]",
    "socio_pension" : "Retired or on early retirement [% of spine cases]",
    "socio_stud" : "Student [% of spine cases]",
    "socio_øvrige" : "Other employment status [% of spine cases]",
    "udd_Grund" : "Highest completed education: Primary school [% of spine cases]",
    "udd_Gym" :  "Highest completed education: High school [% of spine cases]",
    "udd_Erhverv" : "Highest completed education: Vocational education [% of spine cases]",
    "udd_Videregående" : "Highest completed education: Bachelor's. Master's or PhD [% of spine cases]", 
    "udd_KVU" :  "Shorter tertiary degree [% of spine cases]",
    "udd_MVU" : "Medium tertiary degree [% of spine cases]",
    "udd_LVU" : "Longer tertiary degree [% of spine cases]",
    "udd_NA" :  "Unknown edducation level [% of spine cases]",
    "DM54": "Dorsalgia [% of spine cases]",
    "DM51": "Thoracic and lumbar disc disorders [% of spine cases]",
    "DM47": "Spondylosis [% of spine cases]", 
    "DM48": "Other spondylopathies [% of spine cases]",
    "DM50": "Cervical disc disorders [% of spine cases]",
    "DM_other": "Other Diagnoses [% of spine cases]",
    "ryg_pt" : "Patients with Spine problems [Patient count]",
    "Aktions diagnose" : "Main diagnosis [% of spine cases]",
    "rgt" : "X-ray [% of spine cases]",
    "mr" : "MR scan [% of spine cases]",
    "ct" : "CT scan [% of spine cases]",
    "type af behandling" : "Treatment type [% of spine cases]",
    "FP" : "Early Retirement - (førtidspension) [% of spine cases]",
    "Sundhedsråd_kode" : "Health Council code",
    "alder_incident" : "Incident age [Age]",
    "alder_18_34" : "Patients Aged from 18 to 34 [% of spine cases]",
    "alder_35_44" : "Patients Aged from 35 to 44 [% of spine cases]",
    "alder_45_54" : "Patients Aged from 45 to 54 [% of spine cases]",
    "alder_55_64" : "Patients Aged from 55 to 64 [% of spine cases]",
    "alder_65_74" : "Patients Aged from 65 to 74 [% of spine cases]",
    "alder_75_" : "Patients Aged from 75 and up [% of spine cases]",
    "dispon_13" : "Salary [DKK]",
    "Sundhedsråd_navn" : "Health Counsil",
    "bef" : "Population size",
    "incident" : "Incident [Patient count]"

}

display_names_yaxis_translated = {
    "enlig": {
        "da": "Enlig [% af rygpatienter]",
        "en": "Single [% of spine cases]"
    },
    "Civil tilstand": {
        "da": "Civilstand [% af rygpatienter]",
        "en": "Marital status [% of spine cases]"
    },
    "samlev": {
        "da": "Samlevende [% af rygpatienter]",
        "en": "Cohabiting [% of spine cases]"
    },
    "opr_land_dk": {
        "da": "Oprindelsesland: Danmark [% af rygpatienter]",
        "en": "Country of origin: Denmark [% of spine cases]"
    },
    "opr_land_vest": {
        "da": "Oprindelsesland: Vestlige lande [% af rygpatienter]",
        "en": "Country of origin: Western [% of spine cases]"
    },
    "opr_land_ikke_vest": {
        "da": "Oprindelsesland: Ikke-vestlige lande [% af rygpatienter]",
        "en": "Country of origin: Non-Western [% of spine cases]"
    },
    "socio_beskæft": {
        "da": "Selvstændig, ansat eller studerende [% af rygpatienter]",
        "en": "Self-employed, employed or student [% of spine cases]"
    },
    "socio_arbløs": {
        "da": "Arbejdsløs [% af rygpatienter]",
        "en": "Unemployed [% of spine cases]"
    },
    "socio_overførsel": {
        "da": "Modtager offentlig hjælp [% af rygpatienter]",
        "en": "Receiving public help [% of spine cases]"
    },
    "socio_pension": {
        "da": "Pensionist eller førtidspensionist [% af rygpatienter]",
        "en": "Retired or on early retirement [% of spine cases]"
    },
    "socio_stud": {
        "da": "Studerende [% af rygpatienter]",
        "en": "Student [% of spine cases]"
    },
    "socio_øvrige": {
        "da": "Anden beskæftigelse [% af rygpatienter]",
        "en": "Other employment status [% of spine cases]"
    },
    "udd_Grund": {
        "da": "Højest fuldførte uddannelse: Grundskole [% af rygpatienter]",
        "en": "Highest completed education: Primary school [% of spine cases]"
    },
    "udd_Gym": {
        "da": "Højest fuldførte uddannelse: Gymnasial [% af rygpatienter]",
        "en": "Highest completed education: High school [% of spine cases]"
    },
    "udd_Erhverv": {
        "da": "Højest fuldførte uddannelse: Erhvervsuddannelse [% af rygpatienter]",
        "en": "Highest completed education: Vocational education [% of spine cases]"
    },
    "udd_Videregående": {
        "da": "Højest fuldførte uddannelse: Videregående [% af rygpatienter]",
        "en": "Highest completed education: Bachelor's, Master's or PhD [% of spine cases]"
    },
    "udd_KVU": {
        "da": "Kort videregående uddannelse [% af rygpatienter]",
        "en": "Shorter tertiary degree [% of spine cases]"
    },
    "udd_MVU": {
        "da": "Mellemlang videregående uddannelse [% af rygpatienter]",
        "en": "Medium tertiary degree [% of spine cases]"
    },
    "udd_LVU": {
        "da": "Lang videregående uddannelse [% af rygpatienter]",
        "en": "Longer tertiary degree [% of spine cases]"
    },
    "udd_NA": {
        "da": "Ukendt uddannelsesniveau [% af rygpatienter]",
        "en": "Unknown education level [% of spine cases]"
    },
    "DM54": {
        "da": "Dorsalgi [% af rygpatienter]",
        "en": "Dorsalgia [% of spine cases]"
    },
    "DM51": {
        "da": "Thorakal og lumbal diskusprolaps [% af rygpatienter]",
        "en": "Thoracic and lumbar disc disorders [% of spine cases]"
    },
    "DM47": {
        "da": "Spondylose [% af rygpatienter]",
        "en": "Spondylosis [% of spine cases]"
    },
    "DM48": {
        "da": "Andre spondylopatier [% af rygpatienter]",
        "en": "Other spondylopathies [% of spine cases]"
    },
    "DM50": {
        "da": "Cervikal diskusprolaps [% af rygpatienter]",
        "en": "Cervical disc disorders [% of spine cases]"
    },
    "DM_other": {
        "da": "Andre diagnoser [% af rygpatienter]",
        "en": "Other Diagnoses [% of spine cases]"
    },
    "ryg_pt": {
        "da": "Rygpatienter [Antal patienter]",
        "en": "Patients with Spine problems [Patient count]"
    },
    "Aktions diagnose": {
        "da": "Aktionsdiagnose [% af rygpatienter]",
        "en": "Main diagnosis [% of spine cases]"
    },
    "rgt": {
        "da": "Røntgen [% af rygpatienter]",
        "en": "X-ray [% of spine cases]"
    },
    "mr": {
        "da": "MR-scanning [% af rygpatienter]",
        "en": "MR scan [% of spine cases]"
    },
    "ct": {
        "da": "CT-scanning [% af rygpatienter]",
        "en": "CT scan [% of spine cases]"
    },
    "type af behandling": {
        "da": "Behandlingstype [% af rygpatienter]",
        "en": "Treatment type [% of spine cases]"
    },
    "FP": {
        "da": "Førtidspension [% af rygpatienter]",
        "en": "Early Retirement - (førtidspension) [% of spine cases]"
    },
    "Sundhedsråd_kode": {
        "da": "Sundhedsråd kode",
        "en": "Health Council code"
    },
    "alder_incident": {
        "da": "Alder ved incident [Alder]",
        "en": "Incident age [Age]"
    },
    "alder_18_34": {
        "da": "Patienter i alderen 18 til 34 [% af rygpatienter]",
        "en": "Patients aged from 18 to 34 [% of spine cases]"
    },
    "alder_35_44": {
        "da": "Patienter i alderen 35 til 44 [% af rygpatienter]",
        "en": "Patients aged from 35 to 44 [% of spine cases]"
    },
    "alder_45_54": {
        "da": "Patienter i alderen 45 til 54 [% af rygpatienter]",
        "en": "Patients aged from 45 to 54 [% of spine cases]"
    },
    "alder_55_64": {
        "da": "Patienter i alderen 55 til 64 [% af rygpatienter]",
        "en": "Patients aged from 55 to 64 [% of spine cases]"
    },
    "alder_65_74": {
        "da": "Patienter i alderen 65 til 74 [% af rygpatienter]",
        "en": "Patients aged from 65 to 74 [% of spine cases]"
    },
    "alder_75_": {
        "da": "Patienter i alderen 75 og opefter [% af rygpatienter]",
        "en": "Patients aged from 75 and up [% of spine cases]"
    },
    "dispon_13": {
        "da": "Lønindkomst [DKK]",
        "en": "Salary [DKK]"
    },
    "Sundhedsråd_navn": {
        "da": "Sundhedsråd navn",
        "en": "Health Council"
    },
    "bef": {
        "da": "Befolkningstal",
        "en": "Population size"
    },
    "incident": {
        "da": "Incident [Antal patienter]",
        "en": "Incident [Patient count]"
    }
}
def dnt_yaxis(variable, lang):
    return display_names_yaxis_translated.get(variable, {}).get(lang, variable)