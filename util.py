import pandas as pd

def read_excelfile(path:str):
    input_book = pd.ExcelFile(path)
    input_sheet_name = input_book.sheet_names
    assert len(input_sheet_name) == 1
    input_sheet_df = input_book.parse(input_sheet_name[0])
    return input_sheet_df

def _detect_annotation_errors(df, criterion: str) -> list:
    # detect where the num. of sents and the num. of anno. do not match
    if criterion in ['Non-redundancy', 'Fluency']:
        col_name = '待测摘要文本'
    elif criterion == 'Informativeness':
        col_name = '标准答案'
    else:
        raise ValueError()
    ref = ''
    errors = []
    for i, (_ref, cri) in enumerate(zip(df[col_name].values.tolist(), df[criterion])):
        
        if isinstance(_ref, str): 
            # Null _ref are cases where the original file has merged rows
            # In that case, keep the previous text
            ref = _ref
        
        sents = ref.strip().split('。')
        if sents[-1] == '':
            sents = sents[:-1]
        num_sents = len(sents)
        
        if isinstance(cri, int):
            if num_sents != 1:
                errors.append((i, ref))
                print(i, ref)
        else:
            cri = cri.strip().replace(' ', '').replace('，', ',')
            if cri in ['Informativeness', 'Non-redundancy', 'Fluency']:
                # For some reason the original file contains the headers multiple times
                pass    
            elif num_sents != len(cri.split(',')):
                errors.append((i, ref))
                print(i, ref)
    return errors

def detect_annotation_errors(df):
    errors = {'Informativeness': [], 'Non-redundancy': [], 'Fluency': []}
    for k in errors.keys():
        errors[k] = _detect_annotation_errors(df, k)
    return errors
