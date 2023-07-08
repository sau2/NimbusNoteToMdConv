"""
Convert Nimbus Notes JSON to MD
"""

from markdownify import markdownify as md
import json, os, shutil, re


def nimbusNoteToMdConv():
    def subf(v, pd, sh=0):
        if 'elem_type' in v and v['elem_type'] == 'folder':
            fn = os.path.join(pd, v['folder_name'])
            try:
                os.mkdir(fn)
            except:
                pass
            print(' ' * sh, v['folder_name'])
            for n in v["notes"]:
                nn = os.path.join(fn, n["note_title"].translate(str.maketrans("[]{}<>—", "()()()-", "!@#$%^&*+|\/:;")))
                suf, cnr = '', 0
                while os.path.isfile(nn + suf + ".md"):
                    cnr += 1
                    suf = f"_{cnr}"
                nn += suf + ".md"
                f = open(nn, mode="w", encoding="utf-8")
                cnt = n['content_data']
                for i in re.findall(r"#attacheloc:([^#]+)#", cnt):
                    for j in n["attach_list"]:
                        if j["attach_id"] == i:
                            pn = j["pathname"]
                            nm = os.path.basename(pn)
                            shutil.copyfile("D://sau//JP//NimbusNotes" + pn[1:], os.path.join(fn, nm))
                            cnt = cnt.replace(f"#attacheloc:{i}#", nm)
                            break

                f.write(md(cnt, heading_style="ATX"))
                f.close()
                print(' ' * (sh + 4), '>', n["note_title"], len(cnt))
            for j in v["subfolders"]:
                subf(j, fn, sh + 4)
        return

    f = open('D://sau//JP//NimbusNotes//sau270.json', 'r', encoding="utf-8")
    for v in json.load(f):
        if 'elem_type' in v and v['elem_type'] == 'folder' and v['folder_name'] == 'User Folder':
            subf(v, 'D://sau//JP//NimbusNotes//OUT')

    return


nimbusNoteToMdConv()
