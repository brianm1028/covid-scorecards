class Permissions:

    SUPERUSER = 1
    ADMIN = 2
    MANAGER = 4

    DISTRICT = 8
    FACILITY = 16

    PPE = 32
    SPACE = 64
    STAFF = 128
    TRANS = 256

    _lookups ={
        'SUPERUSER':SUPERUSER,
        'ADMIN':ADMIN,
        'MANAGER':MANAGER,
        'DISTRICT':DISTRICT,
        'FACILITY':FACILITY,
        'PPE':PPE,
        'SPACE':SPACE,
        'STAFF':STAFF,
        'TRANS':TRANS,
        1:'SUPERUSER',
        2:'ADMIN',
        4:'MANAGER',
        8:'DISTRICT',
        16:'FACILITY',
        32:'PPE',
        64:'SPACE',
        128:'STAFF',
        256:'TRANS'
    }

    DISTRICT_ADMIN = ADMIN+MANAGER+DISTRICT+PPE+SPACE+STAFF+TRANS
    DISTRICT_MANAGER = MANAGER+DISTRICT+PPE+SPACE+STAFF+TRANS
    DISTRICT_PPE_MANAGER = MANAGER+DISTRICT+PPE
    DISTRICT_SPACE_MANAGER = MANAGER+DISTRICT+SPACE
    DISTRICT_STAFF_MANAGER = MANAGER+DISTRICT+STAFF
    DISTRICT_TRANS_MANAGER = MANAGER+DISTRICT+TRANS
    FACILITY_MANAGER = MANAGER+FACILITY+PPE+SPACE+STAFF+TRANS
    FACILITY_PPE_MANAGER = MANAGER+FACILITY+PPE
    FACILITY_SPACE_MANAGER = MANAGER+FACILITY+SPACE
    FACILITY_STAFF_MANAGER = MANAGER+FACILITY+STAFF

    @staticmethod
    def lookups():
        return Permissions._lookups

    @staticmethod
    def lookup(perm):
        return Permissions._lookups[perm]

    @staticmethod
    def list(permset):
        return [n for p,n in [(i,Permissions._lookups[i]) for i in Permissions._lookups.keys() if type(i)==int] if Permissions.check(p,permset)]

    @staticmethod
    def check(perm, permset):
        if type(permset)==int:
            return (perm == (perm & permset))
        else:
            return False