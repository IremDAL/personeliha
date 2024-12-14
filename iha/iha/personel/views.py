from django.shortcuts import render ,redirect
from django.views.decorators.csrf import csrf_exempt
from fastapi import Response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Q
from streamlit import status
from personel.models import personeladd ,partsadd ,ucakparcasayilari ,ucaklar
from django.contrib.auth.hashers import check_password
import json
from personel.serializers import (
    PersonelSerializer,
    PartsSerializer
    
)
@csrf_exempt
def home(request):
    return render(request, 'personelekle.html')
@csrf_exempt
def login_page(request):
    return render(request, 'login.html')
@csrf_exempt
def personeltransactions(request):
    if request.method == "POST":
        personel_data = JSONParser().parse(request)
        personel_data['password'] = make_password(personel_data['password'])
        personel_serializer = PersonelSerializer(data=personel_data)

        if personel_serializer.is_valid():
            personel_serializer.save()
            return JsonResponse({"message": "Success to Add", "data": personel_serializer.data}, status=201)
        else:
            return JsonResponse({"message": "Invalid data", "errors": personel_serializer.errors}, status=400)
        

@csrf_exempt
def dashboard(request):
    username = request.GET.get('username')
    if username:
        try:
            user = personeladd.objects.get(username=username)
            user_team = user.team
            return render(request, 'dashboard.html',  {'username': username, 'team': user_team})
        except personeladd.DoesNotExist:
            return JsonResponse({'error': 'Kullanıcı bulunamadı!'}, status=404)
    else:
        return JsonResponse({'error': 'Geçersiz istek!'}, status=400)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = personeladd.objects.get(username=username)
            if check_password(password, user.password):
                request.session['selected_team'] = user.team  # Store the team in session
                return JsonResponse({'success': True, 'team': user.team})
            else:
                return JsonResponse({'success': False, 'message': 'Şifre yanlış.'})
        except personeladd.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Kullanıcı bulunamadı.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@csrf_exempt
def add_part(request):
    if request.method == 'POST':
        parts_data = JSONParser().parse(request)
        parts_serializer = PartsSerializer(data=parts_data)
        if parts_serializer.is_valid():
            parts_serializer.save()
            return JsonResponse({"message": "Success to Add", "data": parts_serializer.data}, status=201)
        else:
            return JsonResponse({"message": "Invalid data", "errors": parts_serializer.errors}, status=400)
        
    else:
        form = PartsSerializer() 
        return render(request, 'add_part.html', {'form': form})
@csrf_exempt
def parts_list(request):
    if request.method == 'GET':
        return render(request, 'parts_list.html') 

@csrf_exempt
def get_parts(request):
    if request.method == 'GET':
        team = request.session.get('selected_team')
        print(f"Takım Bilgisi Backend: {team}")
        if not team:
            return JsonResponse({"message": "Takım bilgisi eksik!"}, status=400)

        try:
            parts = partsadd.objects.filter(team=team).values('Id', 'aircraft', 'parts')
            parts_list = list(parts)
            if not parts_list:
                return JsonResponse({"message": "Parça bulunamadı!"}, status=404)

            return JsonResponse({"message": "Parçalar başarıyla listelendi", "data": parts_list}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Hata: {str(e)}"}, status=500)
@csrf_exempt
def update_part(request, part_id):
    if request.method == 'PATCH':
        try:
            part = partsadd.objects.get(Id=part_id)
            part.isDeleted = True
            part.save()

            return JsonResponse({'success': True, 'message': 'Part marked as deleted successfully'}, status=200)

        except partsadd.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Part not found'}, status=404)
@csrf_exempt
def aircraft_produce(request):
    return render(request, 'aircraft_produce.html')
        
@csrf_exempt
def fetch_aircraft_parts(request):
    if request.method == 'GET':
        aircraft_type = request.GET.get('aircraftType')
        if not aircraft_type:
            return JsonResponse({'error': 'Aircraft type is required'}, status=400)

        try:
            parts = partsadd.objects.filter(aircraft=aircraft_type,  isDeleted=False).values('Id', 'parts')
            parts_list = list(parts)
            if not parts_list:
                return JsonResponse({'error': 'No parts found for this aircraft type'}, status=404)

            return JsonResponse({'message': 'Parçalar başarıyla listelendi', 'parts': parts_list}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
@csrf_exempt
def update_part_count(request):
    ucaklar = partsadd.objects.filter(isDeleted=False).values('aircraft').annotate(
        kanat_sayisi=Count('Id', filter=Q(parts='Kanat', isDeleted=False)),
        kuyruk_sayisi=Count('Id', filter=Q(parts='Kuyruk', isDeleted=False)),
        govde_sayisi=Count('Id', filter=Q(parts='Gövde', isDeleted=False)),
        aviyonik_sayisi=Count('Id', filter=Q(parts='Aviyonik', isDeleted=False))
    )

    for ucak in ucaklar:
        parts, created = ucakparcasayilari.objects.update_or_create(
            ucak_adi=ucak['aircraft'],
            defaults={
                'kanat_sayisi': ucak['kanat_sayisi'],
                'kuyruk_sayisi': ucak['kuyruk_sayisi'],
                'govde_sayisi': ucak['govde_sayisi'],
                'aviyonik_sayisi': ucak['aviyonik_sayisi'],
            }
        )

    return JsonResponse({'status': 'success'}, status=200)
 

@csrf_exempt
def aircraft_produced(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aircraft_name = data.get('aircraftName')
            produced_parts = data.get('producedParts')

            if not aircraft_name or not produced_parts:
                return JsonResponse({'error': 'Eksik veri gönderildi.'}, status=400)
            aircraft = ucaklar.objects.create(aircraft=aircraft_name)
            aircraft.partss = json.dumps(produced_parts)
            aircraft.save()

            ucak_parca_sayilari = ucakparcasayilari.objects.filter(ucak_adi=aircraft_name).first()

            if not ucak_parca_sayilari:
                return JsonResponse({'error': f'"{aircraft_name}" için stok bulunamadı.'}, status=404)
            for part_name in produced_parts:
                part_name = part_name.lower() 
                if part_name == 'kanat' and ucak_parca_sayilari.kanat_sayisi > 0:
                    ucak_parca_sayilari.kanat_sayisi -= 1
                    part_entry = partsadd.objects.filter(parts='Kanat', isDeleted=False, aircraft=aircraft_name).first()
                    if part_entry:
                        part_entry.isDeleted = True
                        part_entry.save()
                elif part_name == 'kuyruk' and ucak_parca_sayilari.kuyruk_sayisi > 0:
                    ucak_parca_sayilari.kuyruk_sayisi -= 1
                    part_entry = partsadd.objects.filter(parts='Kuyruk', isDeleted=False, aircraft=aircraft_name).first()
                    if part_entry:
                        part_entry.isDeleted = True
                        part_entry.save()
                elif part_name == 'gövde' and ucak_parca_sayilari.govde_sayisi > 0:
                    ucak_parca_sayilari.govde_sayisi -= 1
                    part_entry = partsadd.objects.filter(parts='Gövde', isDeleted=False, aircraft=aircraft_name).first()
                    if part_entry:
                        part_entry.isDeleted = True
                        part_entry.save()    
                elif part_name == 'aviyonik' and ucak_parca_sayilari.aviyonik_sayisi > 0:
                    ucak_parca_sayilari.aviyonik_sayisi -= 1
                    part_entry = partsadd.objects.filter(parts='Aviyonik', isDeleted=False, aircraft=aircraft_name).first()
                    if part_entry:
                        part_entry.isDeleted = True
                        part_entry.save()          
                else:
                    return JsonResponse({'error': f'{part_name} parçası için yeterli stok bulunmuyor.'}, status=400)

                
                ucak_parca_sayilari.save()

            return JsonResponse({'message': 'Uçak başarıyla üretildi ve stoklar güncellendi.'}, status=201)

        except Exception as e:
            print(str(e)) 
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return render(request, 'aircraft_produced.html')
