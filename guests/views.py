from django.http import JsonResponse
from django.shortcuts import render

from guests.models import Family

# Create your views here.
NO, MR, MRS, FLY = 0, 1, 2, 3


def invite(request, family_id):
    lang = 'g' if request.path.split('/')[-1] == 'g' else 'e'

    if request.method == 'POST':
        invitees = dict(request.POST)
        invitees.pop('csrfmiddlewaretoken')
        invitees = {i: invitees[i][0] for i in invitees}
    elif request.method == 'GET':
        details = Family.objects.get(pk=family_id)
        events = {}

        for i in details.groups.all():
            for l in events:
                events[l].append([])
            for j in i.persons.all():
                for k in j.invitations.all():
                    if k.event.name not in events:
                        events[k.event.name] = [[]]
                    events[k.event.name][-1].append([j.title, j.name, j.senior])

        invitees = {}
        for i in events:
            invitees[i] = []
            groups = events[i]
            for j in groups:
                t = [k[0] for k in j]
                if MR in t and MRS in t and FLY in t:
                    mr = j[t.index(MR)]
                    mrs = j[t.index(MRS)]
                    if mr[2] or mrs[2]:
                        invitees[i].append(f'Smt. & Shri {mr[1]} and Family')
                    else:
                        invitees[i].append(f'Mrs. & Mr. {mr[1]} and Family')
                elif MR in t and MRS in t:
                    mr = j[t.index(MR)]
                    mrs = j[t.index(MRS)]
                    if mr[2] or mrs[2]:
                        invitees[i].append(f'Smt. & Shri {mr[1]}')
                    else:
                        invitees[i].append(f'Mrs. & Mr. {mr[1]}')
                elif MR in t and FLY in t:
                    mr = j[t.index(MR)]
                    if mr[2]:
                        invitees[i].append(f'Shri {mr[1]} and Family')
                    else:
                        invitees[i].append(f'Mr. {mr[1]} and Family')
                elif MRS in t and FLY in t:
                    mrs = j[t.index(MRS)]
                    if mrs[2]:
                        invitees[i].append(f'Smt. {mrs[1]} and Family')
                    else:
                        invitees[i].append(f'Mrs. {mrs[1]} and Family')
                elif MR in t:
                    mr = j[t.index(MR)]
                    if mr[2]:
                        invitees[i].append(f'Shri {mr[1]}')
                    else:
                        invitees[i].append(f'Mr. {mr[1]}')
                elif MRS in t:
                    mrs = j[t.index(MRS)]
                    if mrs[2]:
                        invitees[i].append(f'Smt. {mrs[1]}')
                    else:
                        invitees[i].append(f'Mrs. {mrs[1]}')
                else:
                    invitees[i].append('')

                for n in filter(lambda x: x[0] == NO, j):
                    invitees[i][-1] += f'{" and " if len(invitees[i][-1]) else ""}{n[1]}'

                if invitees[i][-1] == '':
                    return  # Error Page
            invitees[i] = ', '.join(invitees[i])
    else:
        return

    e = sorted(invitees.keys())

    invitees['id'] = family_id

    return JsonResponse(invitees)


def error(request, exception=None):
    return JsonResponse({'error': True, 'exception': exception})
