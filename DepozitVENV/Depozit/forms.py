from django import forms

class TirForm(forms.Form):
    id_tir = forms.IntegerField()
    nr_inmatriculare = forms.CharField(max_length=20)
    nume_sofer= forms.CharField(max_length=40)
    prenume_sofer= forms.CharField(max_length=40)
    telefon_sofer= forms.FloatField()

class editTirForm(forms.Form):
    nr_inmatriculare = forms.CharField(max_length=20)
    nume_sofer= forms.CharField(max_length=40)
    prenume_sofer= forms.CharField(max_length=40)
    telefon_sofer= forms.FloatField()

class JobForm(forms.Form):
    id_job= forms.CharField(max_length=10)
    denumire= forms.CharField(max_length=40)
    salariu= forms.FloatField()

class editJobForm(forms.Form):
    denumire= forms.CharField(max_length=40)
    salariu= forms.FloatField()

class AngajatForm(forms.Form):
    id_angajat= forms.IntegerField()
    nume= forms.CharField(max_length=40)
    prenume= forms.CharField(max_length=40)
    job= forms.CharField(max_length=10)
    nr_telefon= forms.FloatField()
    email= forms.CharField(max_length=40, required=False)

class editAngajatForm(forms.Form):
    nume= forms.CharField(max_length=40)
    prenume= forms.CharField(max_length=40)
    job= forms.CharField(max_length=10)
    nr_telefon= forms.FloatField()
    email= forms.CharField(max_length=40, required=False)

class PoartaForm(forms.Form):
    id_poarta= forms.IntegerField()
    stare_poarta= forms.CharField(max_length=30)

class editPoartaForm(forms.Form):
    stare_poarta= forms.CharField(max_length=30)

class ComandaForm(forms.Form):
    id_comanda= forms.IntegerField()
    data_comanda= forms.CharField()
    tip_comanda= forms.CharField(max_length=20)

class ProdusForm(forms.Form):
    id_produs= forms.IntegerField()
    id_firma= forms.IntegerField()
    nume_produs= forms.CharField(max_length=40)
    nr_paleti= forms.IntegerField()
    produse_per_palet= forms.IntegerField()
    tip_produs= forms.CharField(max_length=20)
    pret_produs= forms.FloatField()

class editProdusForm(forms.Form):
    id_firma= forms.IntegerField()
    nume_produs= forms.CharField(max_length=40)
    nr_paleti= forms.IntegerField()
    produse_per_palet= forms.IntegerField()
    tip_produs= forms.CharField(max_length=20)
    pret_produs= forms.FloatField()

class FirmaForm(forms.Form):
    id_firma= forms.IntegerField()
    nume= forms.CharField(max_length=40)
    data_semnare_contract= forms.CharField()
    data_incheiere_contract= forms.CharField(required=False)
    email= forms.CharField(max_length=40,required=False)
    contact_telefon= forms.FloatField()

class editFirmaForm(forms.Form):
    nume= forms.CharField(max_length=40)
    data_semnare_contract= forms.CharField()
    data_incheiere_contract= forms.CharField(required=False)
    email= forms.CharField(max_length=40,required=False)
    contact_telefon= forms.FloatField()

class ALTLForm(forms.Form):
    id_poarta= forms.IntegerField()
    id_angajat= forms.IntegerField()
    id_tura= forms.IntegerField()
    data= forms.CharField()

class Program_tirForm(forms.Form):
    id_tir= forms.IntegerField()
    id_poarta= forms.IntegerField()
    intrare= forms.CharField()
    iesire= forms.CharField(required=False)

class TransportForm(forms.Form):
    id_tir=forms.IntegerField()
    id_comanda=forms.IntegerField()
    distanta=forms.IntegerField(required=False)

class Produse_comandaForm(forms.Form):
    id_produs=forms.IntegerField()
    id_comanda=forms.IntegerField()
    nr_paleti=forms.IntegerField()