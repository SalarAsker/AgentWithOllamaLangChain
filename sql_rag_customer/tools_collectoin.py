from tools_db_all import (get_order,
                          get_account,
                          get_delivery,
                          get_payment,
                          get_product)

from tools_rag_all import search_company_policies

# All the tools collection
tools_collection = [
    get_order,
    get_account,
    get_delivery,
    get_payment,
    get_product,
    search_company_policies
]

