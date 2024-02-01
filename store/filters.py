from django_filters import rest_framework as filters

from .models import ProductModel


class GeneralProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    manufacturer = filters.CharFilter(field_name="manufacturer", lookup_expr="exact", method='filter_few_values')
    info_type = filters.CharFilter(field_name="info__type", lookup_expr="exact", method='filter_few_values')
    info = filters.CharFilter(method = 'filter_json_field')

    def filter_few_values(self, queryset, name, value):
        few_values = value.split(',')
        return queryset.filter(**({f'{name}__in':few_values}))


    def filter_json_field(self, queryset, name, value):

        print(value)
        
        filters = [pair.split(':') for pair in value.split(';')]

        print(filters)
        

        json_filters = {}
        for key, val in filters:

            if key in json_filters:
                json_filters[key].append(val)
            else:
                json_filters[key] = [val]

        print(json_filters)

        qs = queryset

        for key, val in json_filters.items():
            for value in val:
                if value.lower() == "true" or value.lower() == "false":
                    qs = qs.filter(**{f'info__{key}': value.lower() == "true"})
                elif '[' in value:
                    qs = qs.filter(**{f'info__{key}__contains': value[1:-1].split(',')})
                else:
                    qs = qs.filter(**({f'info__{key}__in':val[0].split(',')}))
            
            #qs = qs.filter(**({f'info__{key}__in':val[0].split(',')}))

        return qs

    class Meta:
        model = ProductModel
        fields = ['price','manufacturer']

'''
class MyCustomCharFilter(filters.CharFilter):
    def filter(self, queryset, value):
        if value in EMPTY_VALUES:
            return queryset
        return self.my_custom_filter_method(qs, value)

    def my_custom_filter_method(self, queryset, value):
        return queryset.filter(**{})
'''
'''
class CPUProductFilter(GeneralProductFilter):

    socket = filters.CharFilter(field_name="info__socket", lookup_expr="exact", method = 'filter_few_values')
    generation = filters.CharFilter(field_name="info__generation", lookup_expr="exact", method = 'filter_few_values')
    core = filters.CharFilter(field_name="info__core", lookup_expr="exact", method = 'filter_few_values')
    num_cores = filters.CharFilter(field_name="info__# of CPU Cores", lookup_expr="exact", method = 'filter_few_values')
    num_threads = filters.CharFilter(field_name="info__# of Threads", lookup_expr="exact", method = 'filter_few_values')
    frequency = filters.CharFilter(field_name="info__frequency", lookup_expr="exact", method = 'filter_few_values')
    mult = filters.BooleanFilter(field_name="info__multiplier unlocked")
    delivery = filters.CharFilter(field_name="info__delivery", lookup_expr="exact", method = 'filter_few_values')
    cooler = filters.CharFilter(field_name="info__cooler", lookup_expr="exact", method = 'filter_few_values')
    int_graph = filters.CharFilter(field_name="info__int_graph", lookup_expr="exact", method = 'filter_few_values')


class GPUProductFilter(GeneralProductFilter):
    for_gpu = filters.CharFilter(field_name="info__forgpu", lookup_expr="exact", method = 'filter_few_values')
    socket = filters.CharFilter(field_name="info__socket", lookup_expr="exact", method = 'filter_few_values')
    chipset = filters.CharFilter(field_name="info__chipset", lookup_expr="exact", method = 'filter_few_values')
    formf = filters.CharFilter(field_name="info__formf", lookup_expr="exact", method = 'filter_few_values')
    memory = filters.CharFilter(field_name="info__memory", lookup_expr="exact", method = 'filter_few_values')
    memory_slots = filters.CharFilter(field_name="info__memory_slots", lookup_expr="exact", method = 'filter_few_values')
    memory_channels = filters.CharFilter(field_name="info__memory_channels", lookup_expr="exact", method = 'filter_few_values')
    max_memory = filters.CharFilter(field_name="info__max_memory", lookup_expr="exact", method = 'filter_few_values')
    frequency = filters.CharFilter(field_name="info__frequency", lookup_expr="exact", method = 'filter_few_values')
    slots = filters.CharFilter(field_name="info__slots", lookup_expr="exact", method = 'filter_few_values')
    video = filters.CharFilter(field_name="info__video ", lookup_expr="exact", method = 'filter_few_values')
    num_m2 = filters.CharFilter(field_name="info__num_m2", lookup_expr="exact", method = 'filter_few_values')
    interface_m2 = filters.CharFilter(field_name="info__interface_m2", lookup_expr="exact", method = 'filter_few_values')
    num_sata = filters.CharFilter(field_name="info__num_sata", lookup_expr="exact", method = 'filter_few_values')
    rgb = filters.BooleanFilter(field_name="info__rgb")
    rgb_header = filters.CharFilter(field_name="info__rgb_header", lookup_expr="exact", method = 'filter_few_values')
    color = filters.CharFilter(field_name="info__color", lookup_expr="exact", method = 'filter_few_values')
    

class MotherBoardProductFilter(GeneralProductFilter):
    pass

class RAMProductFilter(GeneralProductFilter):
    pass

class SSDProductFilter(GeneralProductFilter):
    pass

class HDDProductFilter(GeneralProductFilter):
    pass

class PCCaseProductFilter(GeneralProductFilter):
    pass

class PSUProductFilter(GeneralProductFilter):
    pass

class CoolerProductFilter(GeneralProductFilter):
    pass

class MouseProductFilter(GeneralProductFilter):
    pass

class KeyBoardProductFilter(GeneralProductFilter):
    pass

class HeadPhonesProductFilter(GeneralProductFilter):
    pass

class MicroProductFilter(GeneralProductFilter):
    pass

class AccusticProductFilter(GeneralProductFilter):
    pass

class CameraProductFilter(GeneralProductFilter):
    pass

class MPadProductFilter(GeneralProductFilter):
    pass

class UPSProductFilter(GeneralProductFilter):
    pass

class CableProductFilter(GeneralProductFilter):
    pass

class MonitorProductFilter(GeneralProductFilter):
    pass
'''



class AllWillBeOneFilter(GeneralProductFilter):
	pass

			
			