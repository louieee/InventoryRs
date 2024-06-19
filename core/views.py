from drf_yasg import openapi

# Create your views here.


hard_delete_query = openapi.Parameter("hard_delete", in_=openapi.IN_QUERY,
                                      type=openapi.TYPE_BOOLEAN,
                                      description="When true it deletes the record but when false it sets the "
                                                  "deletion_date")
visibility_query = openapi.Parameter("visibility", in_=openapi.IN_QUERY,
                                     type=openapi.TYPE_STRING,
                                     description="The choices are all deleted and active")

page_query = openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                               description="Used to query pages")
page_size_query = openapi.Parameter("page_size", in_=openapi.IN_QUERY,
                                    type=openapi.TYPE_NUMBER, description="Used to query number of records per page")

