from pycad.system import *
from pycad.runtime import *
from pprint import pprint


replace_lists = [
    [
        {
            "DGFH":"MT",
            "FHGF":"T01",
        },{
            "DGFH":"APT",
            "FHGF":"T04",
        }
    ],
    [
        {
            "DGFH":"PT",
        },{
            "DGFH":"MT",
            "FHGF":"T01",
        }
    ],
]

@command()
def fuck(doc):
    print(type(doc))
    ss = edx.ssget()
    if not ss.ok(): return
    with dbtrans(doc) as tr:
        for i,n in enumerate(ss):
            obj = tr.getobject(n)
            if hasattr(obj,"AttributeCollection"):
                attrs = obj.AttributeCollection
                
                attrs_dict = {}
                attrs_obj_dict = {}
                for attr in attrs:
                    attrRef = tr.getobject(attr)
                    attrs_dict[attrRef.Tag] = attrRef.TextString
                    attrs_obj_dict[attrRef.Tag] = attrRef
                for _replace_list in replace_lists:
                    _check = _replace_list[0]
                    _replace = _replace_list[1]
                    _need_replace = True
                    for _key in _check:
                        if attrs_dict.has_key(_key) and _check[_key] == attrs_dict[_key]:
                            continue
                        _need_replace = False
                        break
                    if _need_replace:
                        for _key in _replace:
                            if attrs_dict.has_key(_key):
                                attrRef = attrs_obj_dict[_key]
                                attrRef.UpgradeOpen()
                                attrRef.TextString = _replace[_key]