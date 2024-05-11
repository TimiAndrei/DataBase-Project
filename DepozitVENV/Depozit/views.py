from django.http import JsonResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.apps import apps
from django.core.paginator import Paginator
from .forms import TirForm
from .forms import editTirForm
from .forms import JobForm
from .forms import editJobForm
from .forms import AngajatForm
from .forms import editAngajatForm
from .forms import PoartaForm
from .forms import editPoartaForm
from .forms import ComandaForm
from .forms import ProdusForm
from .forms import editProdusForm
from .forms import FirmaForm
from .forms import editFirmaForm
from .forms import ALTLForm
from .forms import Program_tirForm
from .forms import TransportForm
from .forms import Produse_comandaForm
import cx_Oracle
import datetime
import os
from django.utils import timezone
PER_PAGE = 10


cx_Oracle.init_oracle_client(lib_dir=r"D:/Oracle_libraries/instantclient_21_8")

def connection():
    conn = cx_Oracle.connect(user=os.environ.get('USER'), password=os.environ.get('PASSWORD'), dsn=os.environ.get('DSN'))
    return conn

def index(request):
    return render(request, 'index.html')

def calculate_total_pages(total_records, per_page):
    return (total_records + per_page - 1) // per_page
############################################################################################
def TirList(request):
    sort_by = request.GET.get('sort_by', 'id_tir')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'nr_inmatriculare')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render() 

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()
    
    search_sql = f"SELECT * FROM Tir WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})


    tiruri = []
    for row in cursor.fetchall():
        tiruri.append({
            "id_tir": row[0],
            "nr_inmatriculare": row[1],
            "nume_sofer": row[2],
            "prenume_sofer": row[3],
            "telefon_sofer": row[4]
        })

    paginator = Paginator(tiruri, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()
    
    search_columns =["id_tir", "nr_inmatriculare", "nume_sofer", "prenume_sofer", "telefon_sofer"]

    return render(request, 'TirList.html', {
            'tiruri': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addTir(request):
    if request.method == 'GET':
        return render(request, 'addTir.html', {'tir':{}})
    if request.method == 'POST':
        form = TirForm(request.POST)
        if form.is_valid():
            id_tir = form.cleaned_data.get("id_tir")
            nr_inmatriculare = form.cleaned_data.get("nr_inmatriculare")
            nume_sofer = form.cleaned_data.get("nume_sofer")
            prenume_sofer = form.cleaned_data.get("prenume_sofer")
            telefon_sofer = form.cleaned_data.get("telefon_sofer")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tir VALUES (:id_tir, :nr_inmatriculare, :nume_sofer, :prenume_sofer, :telefon_sofer)", [id_tir, nr_inmatriculare, nume_sofer, prenume_sofer, telefon_sofer])
        conn.commit()
        conn.close()
        return redirect('TirList')

def updateTir(request, id_tir):
    Tir = []
    conn = connection()
    cursor = conn.cursor()
    id=id_tir
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Tir WHERE id_tir = :id_tir", [id_tir])
        row = cursor.fetchone() 
        Tir.append({"id_tir": row[0], "nr_inmatriculare": row[1], "nume_sofer": row[2], "prenume_sofer": row[3], "telefon_sofer": row[4]})
        conn.close()
        return render(request, 'editTir.html', {
        'tir': Tir[0],
        'nr_inmatriculare': row[1],
        'nume_sofer': row[2],
        'prenume_sofer': row[3],
        'telefon_sofer': row[4],
        'id_tir': row[0]
    })
        
    if request.method == 'POST':
        form = TirForm(request.POST)
        if form.is_valid():
            id_tir = int(form.cleaned_data.get("id_tir"))
            nr_inmatriculare = str(form.cleaned_data.get("nr_inmatriculare"))
            nume_sofer = str(form.cleaned_data.get("nume_sofer"))
            prenume_sofer = str(form.cleaned_data.get("prenume_sofer"))
            telefon_sofer = float(form.cleaned_data.get("telefon_sofer"))
            cursor.execute("UPDATE Tir SET id_tir=:id_tir,  nr_inmatriculare = :nr_inmatriculare, nume_sofer =:nume_sofer, prenume_sofer = :prenume_sofer, telefon_sofer = :telefon_sofer WHERE id_tir = :id", [id_tir, nr_inmatriculare, nume_sofer, prenume_sofer, telefon_sofer, id])
            conn.commit()
        conn.close()
        return redirect('TirList')

def deleteTir(request, id_tir):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tir WHERE id_tir = :id_tir", [id_tir])
    conn.commit()
    conn.close()
    return redirect('TirList')

############################################################################################
def JobList(request):
    sort_by = request.GET.get('sort_by', 'id_job')
    sort_order = request.GET.get('sort_order', 'ASC')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'denumire')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()
    search_sql = f"SELECT * FROM Job WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    jobs = []
    for row in cursor.fetchall():
        jobs.append({"id_job": row[0], "denumire": row[1], "salariu": row[2]})

    paginator = Paginator(jobs, PER_PAGE)
    page_obj = paginator.get_page(page_number)
    conn.close()
    search_columns =["id_job", "denumire", "salariu"]

    return render(request, 'JobList.html', {
            'jobs': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addJob(request):
    if request.method == 'GET':
        return render(request, 'addJob.html', {'job':{}})
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            id_job = form.cleaned_data.get("id_job")
            denumire = form.cleaned_data.get("denumire")
            salariu = form.cleaned_data.get("salariu")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Job VALUES (:id_job, :denumire, :salariu)", [id_job, denumire, salariu])
        conn.commit()
        conn.close()
        return redirect('JobList')

def updateJob(request, id_job):
    Job = []
    conn = connection()
    cursor = conn.cursor()
    id=id_job
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Job WHERE id_job = :id_job", [id_job])
        row = cursor.fetchone() 
        Job.append({"id_job": row[0], "denumire": row[1], "salariu": row[2]})
        conn.close()
        return render(request, 'editJob.html', {
        'job': Job[0],
        'denumire': row[1],
        'salariu': row[2]
    })
        
    if request.method == 'POST':
        form = editJobForm(request.POST)
        if form.is_valid():
            denumire = str(form.cleaned_data.get("denumire"))
            salariu = float(form.cleaned_data.get("salariu"))
            cursor.execute("UPDATE Job SET  denumire = :denumire, salariu = :salariu WHERE id_job = :id_job", [denumire, salariu, id])
            conn.commit()
        conn.close()
        return redirect('JobList')

def deleteJob(request, id_job):
    conn=connection()
    if request.method == 'GET':
        page_number = request.GET.get('page', 1)

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Angajat WHERE job = :id_job", [id_job])
        angajati = []
        for row in cursor.fetchall():
            angajati.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2], "job": row[3], "nr_telefon": row[4], "email": row[5]})
        paginator = Paginator(angajati, PER_PAGE)
        page_obj = paginator.get_page(page_number)
        conn.close()

        return render(request, 'WarningODCJob.html', {'id_job': id_job, 'angajati': page_obj})
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Job WHERE id_job = :id_job", [id_job])
    conn.commit()
    conn.close()
    return redirect('JobList')

############################################################################################

def ListAngajat(request):
    sort_by = request.GET.get('sort_by', 'id_angajat')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'nume')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()
    
    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Angajat WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    angajati = []
    for row in cursor.fetchall():
        angajati.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2], "job": row[3], "nr_telefon": row[4], "email": row[5]})

    paginator = Paginator(angajati, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_angajat", "nume", "prenume", "job", "nr_telefon", "email"]

    return render(request, 'ListAngajat.html', {
            'angajati': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addAngajat(request):
    if request.method == 'GET':
        jobs = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Job")
        for row in cursor.fetchall():
            jobs.append({"id_job": row[0],"denumire": row[1], "salariu": row[2]})
        conn.close()
        return render(request, 'addAngajat.html', {'angajat':{}, 'jobs': jobs})
    
    if request.method == 'POST':
        form = AngajatForm(request.POST)
        if form.is_valid():
            id_angajat = form.cleaned_data.get("id_angajat")
            nume = form.cleaned_data.get("nume")
            prenume = form.cleaned_data.get("prenume")
            job = form.cleaned_data.get("job")
            nr_telefon = form.cleaned_data.get("nr_telefon")
            email = form.cleaned_data.get("email")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Angajat VALUES (:id_angajat, :nume, :prenume, :job, :nr_telefon, :email)", [id_angajat, nume, prenume, job, nr_telefon, email])
        conn.commit()
        conn.close()
        return redirect('ListAngajat')

def updateAngajat(request, id_angajat):
    Angajat = []
    conn = connection()
    cursor = conn.cursor()
    id=id_angajat
    jobs=[]
    cursor.execute("SELECT * FROM Job")
    for row in cursor.fetchall():
        jobs.append({"id_job": row[0],"denumire": row[1], "salariu": row[2]})
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Angajat WHERE id_angajat = :id_angajat", [id_angajat])
        row = cursor.fetchone() 
        Angajat.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2], "job": row[3], "nr_telefon": row[4], "email": row[5]})
        conn.close()
        return render(request, 'editAngajat.html', {
        'angajat': Angajat[0],
        'nume': row[1],
        'prenume': row[2],
        'job': row[3],
        'nr_telefon': row[4],
        'email': row[5],
        'jobs': jobs
    })
        
    if request.method == 'POST':
        form = editAngajatForm(request.POST)
        if form.is_valid():
            nume = str(form.cleaned_data.get("nume"))
            prenume = str(form.cleaned_data.get("prenume"))
            job = str(form.cleaned_data.get("job"))
            nr_telefon = float(form.cleaned_data.get("nr_telefon"))
            email = str(form.cleaned_data.get("email"))
            cursor.execute("UPDATE Angajat SET  nume = :nume, prenume = :prenume, job = :job, nr_telefon = :nr_telefon, email = :email WHERE id_angajat = :id_angajat", [nume, prenume, job, nr_telefon, email, id])
            conn.commit()
        conn.close()
        return redirect('ListAngajat')

def deleteAngajat(request, id_angajat):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Angajat WHERE id_angajat = :id_angajat", [id_angajat])
    conn.commit()
    conn.close()
    return redirect('ListAngajat')

############################################################################################

def ListTura(request):
    ture = []
    conn = connection()
    cursor = conn.cursor()
    sort_order = request.GET.get('sort_order', 'asc')
    cursor.execute("SELECT * FROM Tura ORDER BY id_tura %s" % sort_order)
    for row in cursor.fetchall():
        ture.append({"id_tura": row[0],"ora_incepere": row[1], "ora_sfarsit": row[2]})
    conn.close()
    return render(request, 'ListTura.html', {'ture': ture})

############################################################################################

def ListPoarta(request):
    sort_by = request.GET.get('sort_by', 'id_poarta')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'stare_poarta')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'
    
    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Poarta WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    porti = []
    for row in cursor.fetchall():
        porti.append({"id_poarta": row[0], "stare_poarta": row[1]})
    
    paginator = Paginator(porti, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_poarta", "stare_poarta"]

    return render(request, 'ListPoarta.html', {
            'porti': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addPoarta(request):
    if request.method == 'GET':
        return render(request, 'addPoarta.html', {'poarta':{}})
    if request.method == 'POST':
        form = PoartaForm(request.POST)
        if form.is_valid():
            id_poarta = form.cleaned_data.get("id_poarta")
            stare_poarta = form.cleaned_data.get("stare_poarta")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Poarta VALUES (:id_poarta, :stare_poarta)", [id_poarta, stare_poarta])
        conn.commit()
        conn.close()
        return redirect('ListPoarta')

def updatePoarta(request, id_poarta):
    Poarta = []
    conn = connection()
    cursor = conn.cursor()
    id=id_poarta
    if request.method == 'GET':
        opt=['Descarcare', 'Incarcare', 'Asteptare', 'Liber', 'Finalizat']
        cursor.execute("SELECT * FROM Poarta WHERE id_poarta = :id_poarta", [id_poarta])
        row = cursor.fetchone() 
        Poarta.append({"id_poarta": row[0], "stare_poarta": row[1]})
        conn.close()
        return render(request, 'editPoarta.html', {
        'poarta': Poarta[0],
        'stare_poarta': row[1],
        'opt': opt
    })

    if request.method == 'POST':
        form = editPoartaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            stare_poarta = str(form.cleaned_data.get("stare_poarta"))
            cursor.execute("UPDATE Poarta SET  stare_poarta = :stare_poarta WHERE id_poarta = :id_poarta", [stare_poarta, id])
            conn.commit()
        conn.close()
        return redirect('ListPoarta')

def deletePoarta(request, id_poarta):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Poarta WHERE id_poarta = :id_poarta", [id_poarta])
    conn.commit()
    conn.close()
    return redirect('ListPoarta')

############################################################################################

############################################################################################

def ListComanda(request):
    sort_by = request.GET.get('sort_by', 'id_comanda')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'tip_comanda')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Comanda WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    comenzi = []
    for row in cursor.fetchall():
        comenzi.append({"id_comanda": row[0], "data_comanda": row[1], "tip_comanda": row[2]})

    paginator = Paginator(comenzi, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_comanda", "data_comanda", "tip_comanda"]

    return render(request, 'ListComanda.html', {
            'comenzi': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addComanda(request):
    if request.method == 'GET':
        opt=['Depozitare', 'Livrare']
        return render(request, 'addComanda.html', {'comanda':{}, 'opt':opt})
    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():
            id_comanda = form.cleaned_data.get("id_comanda")
            data_comanda = form.cleaned_data.get("data_comanda")
            if data_comanda =="sysdate":
                data_comanda = datetime.datetime.now()
            tip_comanda = form.cleaned_data.get("tip_comanda")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Comanda VALUES (:id_comanda, :data_comanda, :tip_comanda)", [id_comanda, data_comanda, tip_comanda])
        conn.commit()
        conn.close()
        return redirect('ListComanda')

def deleteComanda(request, id_comanda):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Comanda WHERE id_comanda = :id_comanda", [id_comanda])
    conn.commit()
    conn.close()
    return redirect('ListComanda')

############################################################################################
def ListProdus(request):
    sort_by = request.GET.get('sort_by', 'id_produs')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'nume_produs')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Produs_stoc WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    produse = []
    for row in cursor.fetchall():
        produse.append({"id_produs": row[0], "id_firma": row[1], "nume_produs": row[2], "nr_paleti": row[3], "produse_per_palet": row[4], "tip_produs": row[5], "pret_produs": row[6]})

    paginator = Paginator(produse, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_produs", "id_firma", "nume_produs", "nr_paleti", "produse_per_palet", "tip_produs", "pret_produs"]

    return render(request, 'ListProdus.html', {
            'produse_stoc': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addProdus(request):
    if request.method == 'GET':
        opt=['Detergenti', 'Bauturi', 'Sarate', 'Parfumerie', 'Dulce']
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT id_firma, nume FROM Firma")
        firma=[]
        for row in cursor.fetchall():
            firma.append({"id_firma": row[0], "nume": row[1]})
        conn.close()
        return render(request, 'addProdus.html', {'produs':{}, 'opt':opt, 'firme':firma})
    if request.method == 'POST':
        form = ProdusForm(request.POST)
        if form.is_valid():
            id_produs = form.cleaned_data.get("id_produs")
            id_firma = form.cleaned_data.get("id_firma")
            nume_produs = form.cleaned_data.get("nume_produs")
            nr_paleti = form.cleaned_data.get("nr_paleti")
            produse_per_palet = form.cleaned_data.get("produse_per_palet")
            tip_produs = form.cleaned_data.get("tip_produs")
            pret_produs = form.cleaned_data.get("pret_produs")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Produs_stoc VALUES (:id_produs, :id_firma, :nume_produs, :nr_paleti, :produse_per_palet, :tip_produs, :pret_produs)", [id_produs, id_firma, nume_produs, nr_paleti, produse_per_palet, tip_produs, pret_produs])
        conn.commit()
        conn.close()
        return redirect('ListProdus')

def updateProdus(request,id_produs):
    conn = connection()
    cursor=conn.cursor()
    if request.method == 'GET':
        firme=[]
        cursor.execute("SELECT id_firma, nume FROM Firma")
        for row in cursor.fetchall():
            firme.append({"id_firma": row[0], "nume": row[1]})
        cursor.execute("SELECT * FROM Produs_stoc WHERE id_produs = :id_produs", [id_produs])
        produs = []
        for row in cursor.fetchall():
            produs.append({"id_produs": row[0],"id_firma": row[1], "nume_produs": row[2], "nr_paleti": row[3], "produse_per_palet": row[4], "tip_produs": row[5], "pret_produs": row[6]})
        opt=['Detergenti', 'Bauturi', 'Sarate', 'Parfumerie', 'Dulce']
        conn.close()
        return render(request, 'editProdus.html', {
        'produs': produs[0],
        'id_produs': row[0],
        'id_firma': row[1],
        'nume_produs': row[2],
        'nr_paleti': row[3],
        'produse_per_palet': row[4],
        'tip_produs': row[5],
        'pret_produs': row[6],
        'opt': opt,
        'firme': firme
    })

    if request.method == 'POST':
        form = editProdusForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            id_firma = str(form.cleaned_data.get("id_firma"))
            nume_produs = str(form.cleaned_data.get("nume_produs"))
            nr_paleti = str(form.cleaned_data.get("nr_paleti"))
            produse_per_palet = str(form.cleaned_data.get("produse_per_palet"))
            tip_produs = str(form.cleaned_data.get("tip_produs"))
            pret_produs = str(form.cleaned_data.get("pret_produs"))
            cursor.execute("UPDATE Produs_stoc SET  id_firma = :id_firma, nume_produs = :nume_produs, nr_paleti = :nr_paleti, produse_per_palet = :produse_per_palet, tip_produs = :tip_produs, pret_produs = :pret_produs WHERE id_produs = :id_produs", [id_firma, nume_produs, nr_paleti, produse_per_palet, tip_produs, pret_produs, id_produs])
            conn.commit()
        conn.close()
        return redirect('ListProdus')
    
def deleteProdus(request, id_produs):
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Produs_stoc WHERE id_produs = :id_produs", [id_produs])
        conn.commit()
        conn.close()
        return redirect('ListProdus')

#########################################################################################
def ListFirma(request):
    sort_by = request.GET.get('sort_by', 'id_firma')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'nume')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Firma WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    firme = []
    for row in cursor.fetchall():
        firme.append({"id_firma": row[0], "nume": row[1], "data_semnare_contract": row[2], "data_incheiere_contract": row[3], "email": row[4], "contact_telefon": row[5]})
    
    paginator = Paginator(firme, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_firma", "nume", "data_semnare_contract", "data_incheiere_contract", "email", "contact_telefon"]

    return render(request, 'ListFirma.html', {
            'firme': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addFirma(request):
    if request.method == 'GET':
        return render(request, 'addFirma.html', {'firma':{}})
    if request.method == 'POST':
        form = FirmaForm(request.POST)
        if form.is_valid():
            id_firma = form.cleaned_data.get("id_firma")
            nume = form.cleaned_data.get("nume")
            data_semnare_contract = form.cleaned_data.get("data_semnare_contract")
            data_incheiere_contract = form.cleaned_data.get("data_incheiere_contract")
            email = form.cleaned_data.get("email")
            contact_telefon = form.cleaned_data.get("contact_telefon")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Firma VALUES (:id_firma, :nume, :data_semnare_contract, :data_incheiere_contract, :email, :contact_telefon)", [id_firma, nume, data_semnare_contract, data_incheiere_contract, email, contact_telefon])
        conn.commit()
        conn.close()
        return redirect('ListFirma')

def updateFirma(request,id_firma):
    conn = connection()
    cursor=conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Firma WHERE id_firma = :id_firma", [id_firma])
        firma = []
        for row in cursor.fetchall():
            firma.append({"id_firma": row[0], "nume": row[1], "data_semnare_contract": row[2], "data_incheiere_contract": row[3], "email": row[4], "contact_telefon": row[5]})
        conn.close()
        return render(request, 'editFirma.html', {
        'firma': firma[0],
        'id_firma': row[0],
        'nume': row[1],
        'data_semnare_contract': row[2],
        'data_incheiere_contract': row[3],
        'email': row[4],
        'contact_telefon': row[5]
    })

    if request.method == 'POST':
        form = editFirmaForm(request.POST)
        if form.is_valid():
            nume = str(form.cleaned_data.get("nume"))
            data_semnare_contract = str(form.cleaned_data.get("data_semnare_contract"))
            data_incheiere_contract = str(form.cleaned_data.get("data_incheiere_contract"))
            email = str(form.cleaned_data.get("email"))
            contact_telefon = str(form.cleaned_data.get("contact_telefon"))
            cursor.execute("UPDATE Firma SET  nume = :nume, data_semnare_contract = :data_semnare_contract, data_incheiere_contract = :data_incheiere_contract, email = :email, contact_telefon = :contact_telefon WHERE id_firma = :id_firma", [nume, data_semnare_contract, data_incheiere_contract, email, contact_telefon, id_firma])
            conn.commit()
        conn.close()
        return redirect('ListFirma')
    
def deleteFirma(request, id_firma):
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Firma WHERE id_firma = :id_firma", [id_firma])
        conn.commit()
        conn.close()
        return redirect('ListFirma')

############################################################################################################
def ListALTL(request):
    sort_by = request.GET.get('sort_by', 'id_poarta')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'id_poarta')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Angajat_lucreaza_tura_la_poarta WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    altl = []
    for row in cursor.fetchall():
        altl.append({"id_poarta": row[0], "id_angajat": row[1], "id_tura": row[2], "data": str(row[3])})
    for alt in altl:
        alt['data'] = alt['data'][:len(alt['data'])-9]
        date_obj = datetime.datetime.strptime(alt['data'], '%Y-%m-%d')
        alt['data'] = date_obj.strftime('%d-%b-%Y')
    paginator = Paginator(altl, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_poarta", "id_angajat", "id_tura", "data"]

    return render(request, 'ListALTL.html', {
            'ALTLs': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addALTL(request):
    if request.method == 'GET':
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT id_angajat, nume, prenume FROM Angajat")
        angajati = []
        for row in cursor.fetchall():
            angajati.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2]})
        cursor.execute("SELECT * FROM Tura")
        ture = []
        for row in cursor.fetchall():
            ture.append({"id_tura": row[0], "ora_incepere": row[1], "ora_sfarsit": row[2]})
        cursor.execute("SELECT id_poarta FROM Poarta")
        porti = []
        for row in cursor.fetchall():
            porti.append({"id_poarta": row[0]})
        conn.close()
        return render(request, 'addALTL.html', {'ALTL':{}, 'angajati': angajati, 'ture': ture, 'porti': porti})
    
    if request.method == 'POST':
        form = ALTLForm(request.POST)
        if form.is_valid():
            id_poarta = form.cleaned_data.get("id_poarta")
            id_angajat = form.cleaned_data.get("id_angajat")
            id_tura = form.cleaned_data.get("id_tura")
            data = form.cleaned_data.get("data")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Angajat_lucreaza_tura_la_poarta VALUES (:id_poarta, :id_angajat, :id_tura, :data)", [id_poarta, id_angajat, id_tura, data])
        conn.commit()
        conn.close()
        return redirect('ListALTL')

def updateALTL(request,id_poarta, id_angajat, id_tura, data):
    conn = connection()
    cursor=conn.cursor()
    idp=id_poarta
    ida=id_angajat
    idt=id_tura
    d=data
    porti=[]
    cursor.execute("SELECT id_poarta FROM Poarta")
    for row in cursor.fetchall():
        porti.append({"id_poarta": row[0]})
    
    angajati=[]
    cursor.execute("SELECT id_angajat, nume, prenume FROM Angajat")
    for row in cursor.fetchall():
        angajati.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2]})
    
    ture=[]
    cursor.execute("SELECT * FROM Tura")
    for row in cursor.fetchall():
        ture.append({"id_tura": row[0], "ora_incepere": row[1], "ora_sfarsit": row[2]})

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Angajat_lucreaza_tura_la_poarta WHERE id_poarta = :id_poarta AND id_angajat = :id_angajat AND id_tura = :id_tura AND data = :data", [id_poarta, id_angajat, id_tura, data])
        altl = []
        for row in cursor.fetchall():
            altl.append({"id_poarta": row[0], "id_angajat": row[1], "id_tura": row[2], "data": str(row[3])})
        conn.close()        
        for alt in altl:
            alt['data'] = alt['data'][:len(alt['data'])-9]
            date_obj = datetime.datetime.strptime(alt['data'], '%Y-%m-%d')
            alt['data'] = date_obj.strftime('%d-%b-%Y')
        
        return render(request, 'editALTL.html', {
        'ALTL': altl[0],
        'id_poarta': row[0],
        'id_angajat': row[1],
        'id_tura': row[2],
        'data': row[3],
        'porti': porti,
        'angajati': angajati,
        'ture': ture,
        'ALTLs': altl
    })

    if request.method == 'POST':
        form = ALTLForm(request.POST)
        if form.is_valid():
            id_poarta = form.cleaned_data.get("id_poarta")
            id_angajat = form.cleaned_data.get("id_angajat")
            id_tura = form.cleaned_data.get("id_tura")
            data = form.cleaned_data.get("data")
            cursor.execute("UPDATE Angajat_lucreaza_tura_la_poarta SET  id_poarta = :idp, id_angajat = :ida, id_tura = :id_tura, data = :data WHERE id_poarta = :id_poarta AND id_angajat = :id_angajat AND id_tura = :idt AND data = :d", [id_poarta, id_angajat, id_tura, data, idp, ida, idt, d])
            conn.commit()
        conn.close()
        return redirect('ListALTL')

def deleteALTL(request,id_poarta, id_angajat, id_tura, data):
    conn = connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM Angajat_lucreaza_tura_la_poarta WHERE id_poarta = :id_poarta AND id_angajat = :id_angajat AND id_tura = :id_tura AND data =:data", [id_poarta, id_angajat, id_tura, data])
    conn.commit()
    conn.close()
    return redirect('ListALTL')

############################################################################################################
def ListProgram_tir(request):
    sort_by = request.GET.get('sort_by', 'id_tir')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'id_tir')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Program_tir WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    program_tir = []
    for row in cursor.fetchall():
        program_tir.append({"id_tir": row[0], "id_poarta": row[1], "intrare": str(row[2]), "iesire": str(row[3])})
    for alt in program_tir:
        date_obj = datetime.datetime.strptime(alt['intrare'], '%Y-%m-%d  %H:%M:%S')
        alt['intrare'] = date_obj.strftime('%d-%b-%Y %H:%M:%S')
        if alt['iesire'] != 'None': 
            date_obj = datetime.datetime.strptime(alt['iesire'], '%Y-%m-%d  %H:%M:%S')
            alt['iesire'] = date_obj.strftime('%d-%b-%Y %H:%M:%S')
    paginator = Paginator(program_tir, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_tir", "id_poarta", "intrare", "iesire"]

    return render(request, 'ListProgram_tir.html', {
            'programs': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg
        })

def addProgram_tir(request):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_tir FROM Tir")
    tiri=[]
    for row in cursor.fetchall():
        tiri.append({"id_tir": row[0]})
    cursor.execute("SELECT id_poarta FROM Poarta")
    porti=[]
    for row in cursor.fetchall():
        porti.append({"id_poarta": row[0]})
    if request.method == 'GET':
        conn.close()
        return render(request, 'addProgram_tir.html', {'Program_tir':{}, 'tirs': tiri, 'porti': porti})
    
    if request.method == 'POST':
        form = Program_tirForm(request.POST)
        if form.is_valid():
            id_tir = form.cleaned_data.get("id_tir")
            id_poarta = form.cleaned_data.get("id_poarta")
            intrare = form.cleaned_data.get("intrare")
            iesire = form.cleaned_data.get("iesire")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Program_tir VALUES (:id_tir, :id_poarta, :intrare, :iesire)", [id_tir, id_poarta, intrare, iesire])
        conn.commit()
        conn.close()
        return redirect('ListProgram_tir')

def updateProgram_tir(request, id_tir, id_poarta, intrare):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_tir FROM Tir")
    tiri=[]
    idt=id_tir
    idp=id_poarta
    date_obj = datetime.datetime.strptime(intrare, '%d-%b-%Y  %H:%M:%S')
    intr = date_obj.strftime('%d-%b-%Y %I:%M:%S %p  ')
    for row in cursor.fetchall():
        tiri.append({"id_tir": row[0]})
    cursor.execute("SELECT id_poarta FROM Poarta")
    porti=[]
    for row in cursor.fetchall():
        porti.append({"id_poarta": row[0]})
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Program_tir WHERE id_tir = :id_tir AND id_poarta = :id_poarta", [id_tir, id_poarta])
        program_tir = []
        for row in cursor.fetchall():
            program_tir.append({"id_tir": row[0], "id_poarta": row[1], "intrare": str(row[2]), "iesire": str(row[3])})
        conn.close()
        return render(request, 'editProgram_tir.html', {
        'Program_tir': program_tir[0],
        'id_tir': row[0],
        'id_poarta': row[1],
        'intrare': row[2],
        'iesire': row[3],
        'tiri': tiri,
        'porti': porti,
        'Program_tirs': program_tir
    })

    if request.method == 'POST':
        form = Program_tirForm(request.POST)
        if form.is_valid():
            id_tir = form.cleaned_data.get("id_tir")
            id_poarta = form.cleaned_data.get("id_poarta")
            intrare = form.cleaned_data.get("intrare")
            iesire = form.cleaned_data.get("iesire")
            # date_obj = datetime.datetime.strptime(intrare, '%d-%b-%Y  %H:%M:%S')
            # intrare = date_obj.strftime('%d-%b-%Y %H:%M:%S')
            # iesire = form.cleaned_data.get("iesire")
            # if iesire and iesire!='None':
            #     date_obj = datetime.datetime.strptime(iesire, '%d-%b-%Y  %H:%M:%S')
            #     iesire = date_obj.strftime('%d-%b-%Y %I:%M:%S %p')
            cursor.execute("UPDATE Program_tir SET  id_tir = :idt, id_poarta = :idp, intrare = :intrare, iesire = :iesire WHERE id_tir = :id_tir AND id_poarta = :id_poarta AND intrare=:intr", [id_tir, id_poarta, intrare, iesire, idt, idp,intr])
            conn.commit()
        conn.close()
        return redirect('ListProgram_tir')

def deleteProgram_tir(request, id_tir, id_poarta,intrare):
    conn = connection()
    cursor=conn.cursor()
    date_obj = datetime.datetime.strptime(intrare, '%d-%b-%Y  %H:%M:%S')
    intrare = date_obj.strftime('%d-%b-%Y %I:%M:%S %p')
    cursor.execute("DELETE FROM Program_tir WHERE id_tir = :id_tir AND id_poarta = :id_poarta AND intrare=:intrare", [id_tir, id_poarta,intrare])
    conn.commit()
    conn.close()
    return redirect('ListProgram_tir')

######################################################################################################
def ListTransport(request):
    sort_by = request.GET.get('sort_by', 'id_tir')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'id_tir')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Transport WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    transporturi = []
    for row in cursor.fetchall():
        transporturi.append({"id_tir": row[0], "id_comanda": row[1], "distanta": row[2]})
    cursor.execute("SELECT id_tir from Tir")
    tiruri=[]
    for row in cursor.fetchall():
        tiruri.append({"id_tir":row[0]})
    cursor.execute("SELECT id_comanda from Comanda")
    comenzi=[]
    for row in cursor.fetchall():
        comenzi.append({"id_comanda":row[0]})
    paginator = Paginator(transporturi, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_tir", "id_comanda", "distanta"]

    return render(request, 'ListTransport.html', {
            'transporturi': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg,
            'tiruri':tiruri,
            'comenzi':comenzi
        })

def addTransport(request):
    conn=connection()
    cursor= conn.cursor()
    cursor.execute("SELECT id_tir FROM Tir")
    tiruri=[]
    for row in cursor.fetchall():
        tiruri.append({"id_tir":row[0]})
    
    cursor.execute("SELECT id_comanda FROM Comanda")
    comenzi=[]
    for row in cursor.fetchall():
        comenzi.append({"id_comanda":row[0]})
    
    if request.method == 'GET':
        conn.close()
        return render(request, 'addTransport.html', {'Transport':{}, 'tiruri':tiruri, 'comenzi':comenzi})
    
    if request.method == 'POST':
        form=TransportForm(request.POST)
        if form.is_valid():
            id_tir=form.cleaned_data.get("id_tir")
            id_comanda=form.cleaned_data.get("id_comanda")
            distanta=form.cleaned_data.get("distanta")
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Transport VALUES (:id_tir, :id_comanda, :distanta)", {'id_tir':id_tir, 'id_comanda':id_comanda, 'distanta':distanta})
        conn.commit()
        conn.close()
        return redirect('ListTransport')

def updateTransport(request, id_tir, id_comanda):
    conn=connection()
    cursor= conn.cursor()
    cursor.execute("SELECT id_tir FROM Tir")
    tiruri=[]
    idt=id_tir
    idc=id_comanda
    for row in cursor.fetchall():
        tiruri.append({"id_tir":row[0]})
    cursor.execute("SELECT id_comanda FROM Comanda")
    comenzi=[]
    for row in cursor.fetchall():
        comenzi.append({"id_comanda":row[0]})

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Transport WHERE id_tir = :id_tir AND id_comanda = :id_comanda",[id_tir,id_comanda])
        Transporturi =[]
        for row in cursor.fetchall():
            Transporturi.append({"id_tir": row[0], "id_comanda": row[1], "distanta": str(row[2])})
        conn.close()
        return render(request, 'editTransport.html', {
        'Transport':Transporturi[0],
        'id_tir':row[0],
        'id_comanda':row[1],
        'distanta': row[2], 
        'tiruri':tiruri, 
        'comenzi':comenzi
        })
    
    if request.method == 'POST':
        form=TransportForm(request.POST)
        if form.is_valid():
            id_tir=form.cleaned_data.get("id_tir")
            id_comanda=form.cleaned_data.get("id_comanda")
            distanta=form.cleaned_data.get("distanta")
            cursor.execute("UPDATE Transport SET id_tir = :id_tir, id_comanda=:id_comanda, distanta = :distanta WHERE id_tir = :idt AND id_comanda =:idc",[id_tir,id_comanda,distanta,idt,idc])
            conn.commit()
        conn.close()
        return redirect('ListTransport')

def deleteTransport(request, id_tir, id_comanda):
    conn=connection()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM Transport WHERE id_tir = :id_tir AND id_comanda=:id_comanda",[id_tir,id_comanda])
    conn.commit()
    conn.close()    
    return redirect('ListTransport')

#########################################################################################

def ListProduse_comanda(request):
    sort_by = request.GET.get('sort_by', 'id_produs')
    sort_order = request.GET.get('sort_order', 'asc')
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search_query', '')
    search_column = request.GET.get('search_column', 'id_produs')
    caret_down_svg = get_template('svg/caret-down-fill.svg').render()
    caret_up_svg = get_template('svg/caret-up-fill.svg').render()

    if sort_order == 'ASC':
        new_sort_order = 'DESC'
    else:
        new_sort_order = 'ASC'

    conn = connection()
    cursor = conn.cursor()

    search_sql = f"SELECT * FROM Produse_comanda WHERE LOWER({search_column}) LIKE LOWER(:search_query) ORDER BY {sort_by} {sort_order}"
    cursor.execute(search_sql, {'search_query': f'%{search_query.lower()}%'})

    prods_comanda = []
    for row in cursor.fetchall():
        prods_comanda.append({"id_produs": row[0], "id_comanda": row[1], "nr_paleti": row[2]})
    cursor.execute("SELECT id_produs from Produs_stoc")
    produse=[]
    for row in cursor.fetchall():
        produse.append({"id_produs":row[0]})
    cursor.execute("SELECT id_comanda from Comanda")
    comenzi=[]
    for row in cursor.fetchall():
        comenzi.append({"id_comanda":row[0]})

    paginator = Paginator(prods_comanda, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    conn.close()

    search_columns =["id_produs", "id_comanda", "nr_paleti"]

    return render(request, 'ListProduse_comanda.html', {
            'prods_comanda': page_obj,
            'sort_order': sort_order,
            'sort_by': sort_by,
            'search_columns': search_columns,
            'search_query': search_query,
            'search_column': search_column,
            'new_sort_order': new_sort_order,
            'caret_down_svg': caret_down_svg,
            'caret_up_svg': caret_up_svg,
            'produse':produse,
            'comenzi':comenzi
        })

def addProduse_comanda(request):
    conn=connection()
    cursor= conn.cursor()
    cursor.execute("SELECT id_produs FROM Produs_stoc")
    produse=[]
    for row in cursor.fetchall():
        produse.append({"id_produs":row[0]})
    
    cursor.execute("SELECT id_comanda FROM Comanda")
    comenzi=[]
    for row in cursor.fetchall():
        comenzi.append({"id_comanda":row[0]})
    
    if request.method == 'GET':
        conn.close()
        return render(request, 'addProduse_comanda.html', {'Produse_comanda':{}, 'produse':produse, 'comenzi':comenzi})
    
    if request.method == 'POST':
        form=Produse_comandaForm(request.POST)
        if form.is_valid():
            id_produs=form.cleaned_data.get("id_produs")
            id_comanda=form.cleaned_data.get("id_comanda")
            nr_paleti=form.cleaned_data.get("nr_paleti")
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Produse_comanda VALUES (:id_produs, :id_comanda, :nr_paleti)", {'id_produs':id_produs, 'id_comanda':id_comanda, 'nr_paleti':nr_paleti})
        conn.commit()
        conn.close()
        return redirect('ListProduse_comanda')

def deleteProduse_comanda(request, id_produs, id_comanda):
    conn=connection()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM Produse_comanda WHERE id_produs = :id_produs AND id_comanda=:id_comanda",[id_produs,id_comanda])
    conn.commit()
    conn.close()    
    return redirect('ListProduse_comanda')

#########################################################################################

def ListCerere1(request):
    conn=connection()
    cursor = conn.cursor()
    cursor.execute("""
SELECT com.id_comanda, com.data_comanda, tip_comanda, prod.id_firma, f.nume as Nume_Firma, p.id_produs, nume_produs, p.nr_paleti 
from comanda com
left join produse_comanda p
on com.id_comanda=p.id_comanda
left join produs_stoc prod
on prod.id_produs=p.id_produs
left join firma f
on prod.id_firma=f.id_firma
where tip_comanda='Depozitare' AND f.id_firma=2
ORDER BY com.id_comanda
""") # nu se justifica left join, cand am conditia id_firma=2, nu se pot compara oricum valorile null, deci nu are rost 
    cereri =[]
    for row in cursor.fetchall():
        cereri.append({"id_comanda": row[0], "data_comanda": row[1], "tip_comanda": row[2], "id_firma": row[3], "nume_firma": row[4], "id_produs": row[5], "nume_produs": row[6], "nr_paleti": row[7]})
    conn.close()
    for alt in cereri:
        alt['data_comanda'] = alt['data_comanda'].strftime('%d-%b-%Y')
    return render(request,'ListCerere1.html', {'cereri': cereri})

#####################################################################################
def ListCerere2(request):
    conn=connection()
    cursor = conn.cursor()
    cursor.execute("""
SELECT tip_produs, f.id_firma, nume Nume_firma, SUM(nr_paleti) Nr_total_paleti, AVG(pret_produs) Pret_mediu, COUNT(id_produs) Nr_produse
FROM Produs_stoc p
LEFT JOIN firma f on p.id_firma=f.id_firma
GROUP BY tip_produs, f.id_firma, nume
HAVING AVG(pret_produs)>5
AND SUM(nr_paleti)>100""")
    cereri =[]
    for row in cursor.fetchall():
        cereri.append({"tip_produs": row[0],"id_firma":row[1], "nume_firma": row[2], "nr_total_paleti": row[3], "pret_mediu": row[4], "nr_produse": row[5]})
    conn.close()
    return render(request,'ListCerere2.html', {'cereri': cereri})

#####################################################################################

def ListView1(request):
    conn=connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vizualizare_compusa ORDER BY id_angajat")
    vizualizari =[]
    for row in cursor.fetchall():
        vizualizari.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2], "job": row[3], "nr_telefon": row[4], "email": row[5], "denumire": row[6], "salariu":row[7]})    
    return render(request,'ListView1.html',{'vizualizari': vizualizari})

def addView1(request):
    if request.method == 'GET':
        jobs = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Job")
        for row in cursor.fetchall():
            jobs.append({"id_job": row[0],"denumire": row[1], "salariu": row[2]})
        conn.close()
        return render(request, 'addView1.html', {'View1':{}, 'jobs': jobs})
    
    if request.method == 'POST':
        form=AngajatForm(request.POST)
        if form.is_valid():
            id_angajat=form.cleaned_data.get("id_angajat")
            nume=form.cleaned_data.get("nume")
            prenume=form.cleaned_data.get("prenume")
            job=form.cleaned_data.get("job")
            nr_telefon=form.cleaned_data.get("nr_telefon")
            email=form.cleaned_data.get("email")
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Vizualizare_compusa(id_angajat, nume, prenume, job, nr_telefon, email) VALUES (:id_angajat, :nume, :prenume, :job, :nr_telefon, :email)",[id_angajat,nume,prenume,job,nr_telefon, email])
        conn.commit()
        conn.close()
        return redirect('ListView1')
    
def updateView1(request, id_angajat):
    
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        jobs=[]
        angajat=[]
        cursor.execute("SELECT * FROM Job")
        for row in cursor.fetchall():
            jobs.append({"id_job": row[0],"denumire": row[1], "salariu": row[2]})
        cursor.execute("SELECT * FROM Vizualizare_compusa WHERE id_angajat = :id_angajat",[id_angajat])
        row=cursor.fetchone()
        angajat.append({"id_angajat": row[0], "nume": row[1], "prenume": row[2], "job": row[3], "nr_telefon": row[4], "email": row[5], "denumire": row[6], "salariu":row[7]})

        conn.close()
        return render(request, 'editView1.html', {
            'angajat': angajat[0],
            'id_angajat':row[0],
            'nume':row[1],
            'prenume':row[2],
            'job':row[3],
            'nr_telefon':row[4],
            'email':row[5],
            'denumire':row[6],
            'salariu':row[7], 
            'jobs': jobs})
    
    if request.method == 'POST':
        form=AngajatForm(request.POST)
        if form.is_valid():
            id_angajat=form.cleaned_data.get("id_angajat")
            nume=form.cleaned_data.get("nume")
            prenume=form.cleaned_data.get("prenume")
            job=form.cleaned_data.get("job")
            nr_telefon=form.cleaned_data.get("nr_telefon")
            email=form.cleaned_data.get("email")
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE Vizualizare_compusa SET nume=:nume, prenume=:prenume, job=:job, nr_telefon=:nr_telefon, email=:email WHERE id_angajat=:id_angajat",[nume,prenume,job,nr_telefon,email,id_angajat])
        conn.commit()
        conn.close()
        return redirect('ListView1')

def deleteView1(request, id_angajat):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vizualizare_compusa WHERE id_angajat=:id_angajat",[id_angajat])
    conn.commit()
    conn.close()
    return redirect('ListView1')


#####################################################################################

def ListView2(request):
    conn=connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vizualizare_complexa")
    vizualizari =[]
    for row in cursor.fetchall():
        vizualizari.append({"id_firma": row[0],"Nume_Firma":row[1], "tip_produs": row[2], "Nr_total_paleti": row[3], "Nr_produse": row[4]})
    return render(request,'ListView2.html',{'vizualizari': vizualizari})

