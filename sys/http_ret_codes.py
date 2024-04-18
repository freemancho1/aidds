# 
# Return code for web service
#

# Ok of GET service
OK = 200                    
HC200 = 'ok'

# Ok of POST service
CREATED = 201               
CR = 201                    
HC201 = 'cr'

# Ok of GET service(without return value)
NO_CONTENT = 204            
NC = 204                    
HC204 = 'nc'

# The server does not understand the client's request info.
BAD_REQUEST = 400           
BR = 400                    
HC400 = 'br'

# The server could not verify 
# that you are authorized to access the URL requested.
UNAUTHORIZED = 401          
UA = 401                    
HC401 = 'ua'

# You don't have the permission to access the requested resource. 
# It is either read-protected or not readable by the server.
FORBIDDEN = 403             
FB = 403                    
HC403 = 'fb'

# The requested URL was not found on the server.
NOT_FOUND = 404             
NF = 404                    
HC404 = 'nf'

# No access permission for the requested method
METHOD_NOT_ALLOWED = 405    
MNA = 405                   
HC405 = 'mna'

# Internal Server Error 
INTERNAL_SERVER_ERROR = 500 
ISE = 500                   
HC500 = 'ise'