# coding=utf-8
import datetime
import json
import urllib
import time

# 阿里巴巴SDK

from topsdk.ability2940.ability2940 import Ability2940
from topsdk.client import TopApiClient,TopException

# 项目模块
from mylog import MyLog
import upublic
from config import save_config  # 用于更新配置


def create_ability(appkey, appsecret, gateway_url='http://gw.api.taobao.com/router/rest'):
    """创建阿里巴巴接口客户端"""
    client = TopApiClient(
        appkey=appkey,
        app_sercet=appsecret,
        top_gateway_url=gateway_url,
        verify_ssl=False
    )
    return Ability2940(client=client)


def get_name_ex(ent_name_in, ability_in):
    """根据企业名获取企业ID信息（旧接口）"""
    try:
        MyLog.info('EX根据发货企业名, 获取发货企业ID')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_query_getentinfo_request import (
            AlibabaAlihealthDrugtraceTopYljgQueryGetentinfoRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgQueryGetentinfoRequest()
        request_in.ent_name = upublic.extract_hospital_name(ent_name_in)
        MyLog.info(f'查询企业信息入参: {ent_name_in}')

        response = ability_in.alibaba_alihealth_drugtrace_top_yljg_query_getentinfo(request_in)
        MyLog.info(f'查询企业信息返回: {str(response)}')

        if 'ref_ent_id' not in str(response):
            return '未查到该发货企业的ID信息'

        ref_ent_id_out = response['result']['model']['ref_ent_id']
        third_ent_id_out = response['result']['model']['ent_id']
        from_name_out = upublic.extract_hospital_name(ent_name_in)
        MyLog.info(
            f'ex根据发货企业名{ent_name_in}, 获取发货企业ref_ent_id={ref_ent_id_out}, ent_id={third_ent_id_out}'
        )
        return from_name_out, third_ent_id_out, ref_ent_id_out, ref_ent_id_out  # 注意原代码返回值顺序

    except Exception as e:
        error_msg = f'ex根据发货企业名获取ID异常：{str(e)}'
        MyLog.info(error_msg)
        return error_msg


def get_name_new(ent_name_in, ref_ent_id_in, ability_in):
    """根据企业名获取企业ID信息（新接口）"""
    try:
        MyLog.info('new根据发货企业名, 获取发货企业ID')
        from topsdk.ability2940.request.alibaba_alihealth_drug_yljg_getentinfolist_request import (
            AlibabaAlihealthDrugYljgGetentinfolistRequest,
            AlibabaAlihealthDrugYljgGetentinfolistTopEntInfoReqDto
        )
        request_param = AlibabaAlihealthDrugYljgGetentinfolistTopEntInfoReqDto()
        request_param.ent_name = upublic.extract_hospital_name(ent_name_in)
        request_in = AlibabaAlihealthDrugYljgGetentinfolistRequest()
        request_in.query_param = request_param
        request_in.ref_ent_id = ref_ent_id_in

        MyLog.info(f'查询企业信息入参: {ent_name_in}')
        response = ability_in.alibaba_alihealth_drug_yljg_getentinfolist(request_in)
        MyLog.info(f'查询企业信息返回: {str(response)}')

        if 'ref_ent_id' not in str(response):
            return '未查到该发货企业的ID信息'

        from_id_out = response['result']['model'][0]['ref_ent_id']
        ref_ent_id = response['result']['model'][0]['ref_ent_id']
        third_ent_id_out = response['result']['model'][0]['ent_id']
        from_name_out = upublic.extract_hospital_name(ent_name_in)
        MyLog.info(
            f'根据发货企业名{from_name_out}, 获取发货企业ref_ent_id={from_id_out}, ent_id={third_ent_id_out}'
        )
        return from_name_out, third_ent_id_out, from_id_out, ref_ent_id

    except Exception as e:
        error_msg = f'根据发货企业名获取ID异常：{str(e)}'
        MyLog.info(error_msg)
        return error_msg


def handle_interface_request(interface_id, request, confile):
    """处理所有接口请求（根据interface_id分发）"""
    # 解析配置
    appkey = confile.get('ZFB', 'appkey')
    appsecret = confile.get('ZFB', 'appsecret')
    ref_user_id = confile.get('ZFB', 'ref_user_id')
    ref_ent_id = confile.get('ZFB', 'ref_ent_id')
    ent_id = confile.get('ZFB', 'ent_id')

    # 获取请求参数
    in_value = request.form.get('invalue') if interface_id not in ('1', '4') else None
    if in_value:
        in_value = urllib.parse.unquote(in_value, encoding='utf-8', errors='replace')
        MyLog.info(f'收到的原始参数: {in_value}')

    # 创建接口客户端
    ability = create_ability(appkey, appsecret)

    # 1. 企业ID查询（1和4）
    if interface_id in ('1', '4'):
        ent_name = confile.get('ZFB', 'ent_name') if interface_id == '1' else request.form.get('in_name')
        result = get_name_ex(ent_name, ability)
        if isinstance(result, tuple):
            # 更新配置
            save_config('config.conf', {
                'ZFB': {
                    'ent_id': result[3],
                    'ref_ent_id': result[3],
                    'ref_user_id': result[3]
                }
            })
            return f'{result[0]},{result[1]},{result[2]},{result[3]}'
        return result

    # 其他接口需要解析in_value
    if not in_value:
        MyLog.info('没有输入参数')
        return '没有输入参数'
    in_value = eval(in_value)  # 注意：eval有安全风险，建议替换为json.loads

    # 10. 按供应商入库获取追溯码
    if interface_id == '10':
        return handle_interface_10(in_value, ability, ref_ent_id, ent_id, ref_user_id)

    # 8/9. 大箱入库及解析小码
    if interface_id in ('8', '9'):
        return handle_interface_8_9(in_value, ability, ref_ent_id, ent_id, ref_user_id, interface_id)

    # 7. 单据状态查询
    if interface_id == '7':
        return handle_interface_7(in_value, ability, ref_ent_id, ent_id)

    # 2/5. 零售单据上传
    if interface_id in ('2', '5'):
        return handle_interface_2_5(in_value, ability, ref_user_id, interface_id)

    # 3/6. 出入库单据上传
    if interface_id in ('3', '6'):
        return handle_interface_3_6(in_value, ability, ref_user_id, ent_id, request, interface_id)

    return f'未知接口ID: {interface_id}'


def handle_interface_10(in_value, ability, ref_ent_id, ent_id, ref_user_id):
    """处理10号接口：按供应商入库获取追溯码"""
    try:
        MyLog.info('根据发货企业名, 获取发货企业ID')
        a, b, c, d = get_name_ex(in_value['ent_name'], ability)
        from_id = c
        third_ent_id = b
        from_name = a

        # 查询单据明细
        MyLog.info('通过单据号获取追溯码')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_listupout_detail_request import (
            AlibabaAlihealthDrugtraceTopYljgListupoutDetailRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgListupoutDetailRequest()
        request_in.ref_ent_id = ref_ent_id
        request_in.bill_code = in_value['code']
        request_in.from_ref_user_id = from_id
        request_in.to_ref_user_id = ref_ent_id
        response = ability.alibaba_alihealth_drugtrace_top_yljg_listupout_detail(request_in)
        MyLog.info(f'10号接口返回原始参数：{str(response)}')

        # 校验结果
        if 'msg_code' not in response.get('result', {}) or response['result']['msg_code'] != 'SUCCESS':
            return f'按供应商入库获取追溯码失败, {str(response)}'
        if 'model' not in response.get('result', {}):
            return f'按供应商入库获取追溯码失败, 未返回明细, {str(response)}'

        # 解析追溯码
        skey_all = ''
        for drug_info in response['result']['model']['drug_infos_dto_list']:
            for code_info in drug_info['code_info_list_dto_list']:
                if code_info['code_level'] != '1':
                    skey_all += f"{code_info['code']},"
        skey_all = skey_all.rstrip(',')

        # 批量上传入库
        if skey_all:
            from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill_request import (
                AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest
            )
            request_in = AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest()
            request_in.bill_code = f'HIS_gysdh_in{upublic.get_current_time_ms()}'
            request_in.bill_time = datetime.datetime.now()
            request_in.bill_type = 102
            request_in.physic_type = 3
            request_in.ref_user_id = ref_user_id
            request_in.from_user_id = third_ent_id
            request_in.to_user_id = ent_id
            request_in.trace_codes = [skey_all]
            request_in.client_type = '2'
            MyLog.info(f'大箱入库批量上传入参: {str(request_in.to_dict())}')
            response_up = ability.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill(request_in)
            time.sleep(upublic.get_int(10, 11))  # 等待处理
            MyLog.info(f'大箱入库返回: {str(response_up)}')
        else:
            MyLog.info(f'全部为小包装: {from_name}')

        # 构建返回数据
        aoutjson_all = {'Data': []}
        for drug_info in response['result']['model']['drug_infos_dto_list']:
            aoutjson = {
                'BarNo': [],
                'BBY04': '',
                'Quantity': drug_info['least_pkg_amount'],
                'PurchasePrice': '',
                'PresellPrice': '',
                'ProduceDate': drug_info['produce_date'],
                'ExpiryDate': drug_info['valid_end_date'],
                'BBE02': drug_info['product_ent_name'],
                'BatchNo': drug_info['produce_batch_no']
            }
            # 解析小码
            for code_info in drug_info['code_info_list_dto_list']:
                if code_info['code_level'] == '1':
                    aoutjson['BarNo'].append(code_info['code'])
                else:
                    # 大码解析小码
                    from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_query_relation_request import (
                        AlibabaAlihealthDrugtraceTopYljgQueryRelationRequest
                    )
                    request_in = AlibabaAlihealthDrugtraceTopYljgQueryRelationRequest()
                    request_in.ref_ent_id = ref_ent_id
                    request_in.code = code_info['code']
                    request_in.des_ref_ent_id = ref_ent_id
                    response_c = ability.alibaba_alihealth_drugtrace_top_yljg_query_relation(request_in)
                    MyLog.info(f'大码解析小码入参: {str(request_in.to_dict())}')
                    if 'FAIL_BIZ_NOT_CURRENT_OPERATE_CODE' in str(response_c):
                        MyLog.info(f'大码解析异常: {from_name}{code_info["code"]}, 返回{str(response_c)}')
                    # 提取小码
                    for rel in response_c['result']['model_list'][0]['code_relation_list']:
                        if rel['code'] != code_info['code'] and str(rel['code_pack_level']) == '1':
                            aoutjson['BarNo'].append(rel['code'])
            aoutjson_all['Data'].append(aoutjson)
        return json.dumps(aoutjson_all)

    except TopException as e:
        MyLog.info(f'10号接口异常: {str(e)}')
        return str(e)


def handle_interface_8_9(in_value, ability, ref_ent_id, ent_id, ref_user_id, interface_id):
    """处理8/9号接口：大箱入库及解析小码"""
    try:
        # 获取上游企业信息
        MyLog.info('获取上游企业出库单')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_query_upbillcode_request import (
            AlibabaAlihealthDrugtraceTopYljgQueryUpbillcodeRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgQueryUpbillcodeRequest()
        request_in.code = in_value['code']
        request_in.ref_ent_id = ref_ent_id
        response = ability.alibaba_alihealth_drugtrace_top_yljg_query_upbillcode(request_in)
        MyLog.info(f'上游企业出库单返回: {str(response)}')

        # 解析企业ID
        from_id = from_name = third_ent_id = ''
        if len(response['result']['model_list']) > 0:
            from_id = response['result']['model_list'][0]['from_ref_user_id']
            from_name = response['result']['model_list'][0]['from_user_name']
        else:
            a, b, c, d = get_name_ex(in_value['ent_name'], ability)
            from_id = b
            from_name = a


        # 大箱入库上传
        MyLog.info('大箱入库上传')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill_request import (
            AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest()
        request_in.bill_code = f'HIS_dx_in_{in_value["code"]}'
        request_in.bill_time = datetime.datetime.now()
        request_in.bill_type = 102
        request_in.physic_type = 3
        request_in.ref_user_id = ref_user_id
        request_in.from_user_id = from_id
        request_in.to_user_id = ent_id
        request_in.trace_codes = [in_value['code']]
        request_in.client_type = '2'
        response = ability.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill(request_in)
        time.sleep(upublic.get_int(3, 11))  # 等待处理
        MyLog.info(f'8/9大箱入库上传返回: {str(response)}')

        # 大码解析小码
        MyLog.info('大码解析小码')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_query_relation_request import (
            AlibabaAlihealthDrugtraceTopYljgQueryRelationRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgQueryRelationRequest()
        request_in.ref_ent_id = ref_ent_id
        request_in.code = in_value['code']
        request_in.des_ref_ent_id = ref_ent_id
        response = ability.alibaba_alihealth_drugtrace_top_yljg_query_relation(request_in)
        MyLog.info(f'大码解析小码返回: {str(response)}')

        # 构建返回数据
        aoutjson = {
            'BarNo': [],
            'BBY04': '',
            'Quantity': response['result']['model_list'][0]['produce_info_list'][0]['pkg_amount'],
            'PurchasePrice': '',
            'PresellPrice': '',
            'ProduceDate': response['result']['model_list'][0]['produce_info_list'][0]['produce_date'],
            'ExpiryDate': upublic.convert_date_format(
                str(response['result']['model_list'][0]['produce_info_list'][0]['expire_date'])),
            'BBE02': from_name,
            'BatchNo': response['result']['model_list'][0]['produce_info_list'][0]['batch_no']
        }
        # 处理小码列表
        if len(response['result']['model_list'][0]['code_relation_list']) == 1:
            aoutjson['BarNo'].append(in_value['code'])
        else:
            for rel in response['result']['model_list'][0]['code_relation_list']:
                if rel['code'] != in_value['code'] and str(rel['code_pack_level']) == '1':
                    aoutjson['BarNo'].append(rel['code'])

        # 返回JSON格式
        result = json.dumps(aoutjson)
        if interface_id == '8':
            from flask import Response
            resp = Response(result)
            resp.headers['Content-type'] = 'application/json'
            return resp
        return result

    except TopException as e:
        MyLog.info(f'8/9号接口异常: {str(e)}')
        return str(e)


def handle_interface_7(in_value, ability, ref_ent_id, ent_id):
    """处理7号接口：单据状态查询"""
    try:
        MyLog.info('上传单据后处理状态查询')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_query_billstatus_request import (
            AlibabaAlihealthDrugtraceTopYljgQueryBillstatusRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgQueryBillstatusRequest()
        request_in.ref_ent_id = ref_ent_id
        request_in.begin_date = in_value['begin_date']
        request_in.end_date = in_value['end_date']
        request_in.bill_type = in_value['bill_type']
        request_in.page_size = in_value['page_size']
        request_in.page = in_value['page']
        request_in.bill_code = in_value['bill_code']
        request_in.drug_type = '1'
        request_in.from_user_id = ent_id

        MyLog.info(f'7号接口入参: {str(request_in.to_dict())}')
        response = ability.alibaba_alihealth_drugtrace_top_yljg_listupout(request_in)  # 注意原代码此处可能笔误
        MyLog.info(f'7号接口返回: {str(response)}')
        return str(response)

    except TopException as e:
        MyLog.info(f'7号接口异常: {str(e)}')
        return str(e)


def handle_interface_2_5(in_value, ability, ref_user_id, interface_id):
    """处理2/5号接口：零售单据上传"""
    try:
        interface_name = '零售单据上传'
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_uploadretail_request import (
            AlibabaAlihealthDrugtraceTopYljgUploadretailRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgUploadretailRequest()
        request_in.bill_type = 116 if interface_id == '5' else int(in_value['bill_type'])  # 5=退入
        request_in.bill_code = in_value['bill_code']
        request_in.bill_time = datetime.datetime.now()
        request_in.physic_type = 3
        request_in.ref_user_id = ref_user_id
        request_in.from_user_id = ''
        request_in.oper_ic_code = in_value.get('oper_ic_code', '')
        request_in.oper_ic_name = in_value['oper_ic_name']
        request_in.trace_codes = [in_value['trace_codes']]
        request_in.customer_id_type = in_value['customer_id_type']
        request_in.customer_id = in_value['customer_id']
        request_in.user_tel = in_value['user_tel']
        request_in.network_bill_flag = ''
        request_in.medic_doctor = in_value['medic_doctor']
        request_in.medic_dispenser = in_value['medic_dispenser']
        request_in.user_name = in_value['user_name']
        request_in.user_agent = ''

        MyLog.info(f'{interface_name}入参: {str(request_in.to_dict())}')
        response = ability.alibaba_alihealth_drugtrace_top_yljg_uploadretail(request_in)
        MyLog.info(f'{interface_id}号接口返回: {str(response)}')
        return str(response)

    except TopException as e:
        MyLog.info(f'{interface_id}号接口异常: {str(e)}')
        return str(e)


def handle_interface_3_6(in_value, ability, ref_user_id, ent_id, request, interface_id):
    """处理3/6号接口：出入库单据上传"""
    try:
        interface_name = '出入库单据上传'
        third_id = request.form.get('in_name')
        from topsdk.ability2940.request.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill_request import (
            AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest
        )
        request_in = AlibabaAlihealthDrugtraceTopYljgUploadinoutbillRequest()
        request_in.bill_code = in_value['bill_code']
        request_in.bill_time = datetime.datetime.now()
        request_in.bill_type = 102 if interface_id == '3' else 202  # 3=入，6=出
        request_in.physic_type = 3
        request_in.ref_user_id = ref_user_id

        # 设置收发方ID
        if interface_id == '3':
            request_in.from_user_id = third_id
            request_in.to_user_id = ent_id
        elif interface_id == '5':
            request_in.from_user_id = ent_id
            request_in.to_user_id = ent_id
        elif interface_id == '6':
            request_in.from_user_id = ent_id
            request_in.to_user_id = third_id

        # 其他参数
        request_in.dest_user_id = ''
        request_in.oper_ic_code = in_value.get('oper_ic_code', '')
        request_in.oper_ic_name = in_value['oper_ic_name']
        request_in.warehouse_id = ''
        request_in.drug_id = in_value['drug_id']
        request_in.trace_codes = [in_value['trace_codes']]
        request_in.client_type = '2'
        request_in.return_reason_code = in_value['return_reason_code']
        request_in.return_reason_des = in_value['return_reason_des']
        request_in.cancel_reason_code = in_value['cancel_reason_code']
        request_in.cancel_reason_des = in_value['cancel_reason_des']
        request_in.executer_name = in_value['executer_name']
        request_in.executer_code = in_value['executer_code']
        request_in.superviser_name = in_value['superviser_name']
        request_in.superviser_code = in_value['superviser_code']
        request_in.from_address = in_value['from_address']
        request_in.to_address = in_value['to_address']
        request_in.from_bill_code = in_value['from_bill_code']
        request_in.order_code = in_value['order_code']
        request_in.from_person = in_value['from_person']
        request_in.to_person = in_value['to_person']
        request_in.dis_ref_ent_id = ref_user_id
        request_in.dis_ent_id = ent_id
        request_in.qu_receivable = 0
        request_in.xt_is_check = in_value['xt_is_check']
        request_in.xt_check_code = in_value['xt_check_code']
        request_in.xt_check_code_desc = in_value['xt_check_code_desc']
        request_in.drug_list_json = '[]'
        request_in.ass_ref_ent_id = in_value['ass_ref_ent_id']
        request_in.ass_ent_id = in_value['ass_ent_id']

        MyLog.info(f'{interface_name}入参: {str(request_in.to_dict())}')
        response = ability.alibaba_alihealth_drugtrace_top_yljg_uploadinoutbill(request_in)
        MyLog.info(f'{interface_id}号接口返回: {str(response)}')
        return str(response)

    except TopException as e:
        MyLog.info(f'{interface_id}号接口异常: {str(e)}')
        return str(e)