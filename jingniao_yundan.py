import requests, json, datetime, random, math

wx_domain_test = 'http://sandbox.api.whalebird-tranship.com'
yw_domain_test = 'http://sandbox.yw.whalebird-tranship.com'

wx_domain_prd = 'https://wxapi.whalebird-tranship.com'
yw_domain_prd = 'https://yunwei.whalebird-tranship.com'

#BA00000333
wx_token_test2 = '''eyJhbGciOiJIUzUxMiJ9.eyJjcmVhdGVkIjoxNjcwODI3NDE4MTgyLCJzeXNVc2VyV3htcElkIjpudWxsLCJ1c2VydHlwZSI6IkFwcCIsInNvdXJjZXR5cGUiOiJUaGlyZCIsInVzZXJOYW1lIjpudWxsLCJleHAiOjE2NzA4Mjc1MzgsInVzZXJJZCI6IjEwMDI1MTUyNTE3MTcwODMxMzYiLCJncm91cCI6ImEzMDliOWMzLWJlY2MtNGJiNS1hYWY5LTgyNzMzZTVlZjZkZiJ9.meNY6iDxDwQpJbbZBtsb5Oag9Get_4YQFV-24zX7KhmWqADQew9CMSZu08RVz97aVyXIpC7kwkDAWRph2DvKrw'''
wx_token_test1 = '''eyJhbGciOiJIUzUxMiJ9.eyJjcmVhdGVkIjoxNjcxMDExMzYzOTQyLCJzeXNVc2VyV3htcElkIjpudWxsLCJ1c2VydHlwZSI6IkFwcCIsInNvdXJjZXR5cGUiOiJUaGlyZCIsInVzZXJOYW1lIjpudWxsLCJleHAiOjE2NzEwMTE0ODMsInVzZXJJZCI6IjEwNDc4ODMwNzgwNzg0MzUzMjgiLCJncm91cCI6ImZlYjNkOGZkLTdlNDctNGM0Zi1hNDk3LTQzOTVkYzFmNmIxMiJ9.l8ShzvEK5kGZdl3S_zEYttotBTPVUk_JwREkuouPckKlWtAEOSI5YNLSZfhXNgyzQowt9vKETTQSS3_57Mlv8Q'''
#BA00000444
wx_token_test = '''eyJhbGciOiJIUzUxMiJ9.eyJjcmVhdGVkIjoxNjcxMDcxMzU2ODU1LCJzeXNVc2VyV3htcElkIjpudWxsLCJ1c2VydHlwZSI6IkFwcCIsInNvdXJjZXR5cGUiOiJUaGlyZCIsInVzZXJOYW1lIjpudWxsLCJleHAiOjE2NzEwNzE0NzYsInVzZXJJZCI6IjEwNDc4ODMwNzgwNzg0MzUzMjgiLCJncm91cCI6IjM1YWU5NzkzLTBjMTEtNDE4Yy05Y2FmLTliMzZjOTMxZTYxOSJ9.fLJ2elbT5HRSjj0AzFXj6FAlKjznyYePVFQE2gIZGPxcpITRcLFpX7AnyfAuvnpwsFXGrkmUb7ChJKlXysi3og'''

yw_token_test = '''eyJhbGciOiJIUzUxMiJ9.eyJjcmVhdGVkIjoxNjcwODExMjc0MzY1LCJzeXNVc2VyV3htcElkIjpudWxsLCJ1c2VydHlwZSI6bnVsbCwic291cmNldHlwZSI6Ill1bndlaSIsInVzZXJOYW1lIjoiYWRtaW4iLCJleHAiOjE2NzA4MTEzOTQsInVzZXJJZCI6IjIzNDIzNDIiLCJncm91cCI6IjdjMmUxYTI3LWM4NzctNGQzYi1iMWM3LTI2MmM1ZGQxMGEyMSJ9.TztIvuwld0nVHA_mRc8O3eH8kTw4PXfhEOOp0awmj6GSEYfm7JNy7-duUBYJ4tW2Dwk-4UlxqqAtisgfNt1LZQ'''

wx_header = {"Authorization": wx_token_test}
yw_header = {"Authorization": yw_token_test}


def GBK2312(num):  #随机汉字
    randomstr = ''
    for i in range(num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x} {body:x}'
        str = bytes.fromhex(val).decode('gb2312', errors="ignore")
        randomstr += str
    return randomstr


def create_parcel(parcelnum):
    global start_num
    tracking_number_list = []
    tracking_number_header = datetime.datetime.now().strftime('%Y%m%d%H%M')
    parcels = []
    for i in range(parcelnum):
        start_num += 1
        tracking_number = tracking_number_header + (3 - len(str(start_num))) * '0' + str(start_num)
        tracking_number_list.append(tracking_number)
        parcels.append({"isClaim": False,
                        "key": 1,
                        "localTrackingNumber": tracking_number,
                        "parcelPackingMethod": random.randint(0, 3),
                        "productName": "测试物品名称:" + GBK2312(5),
                        "productPrice": random.randint(1, 1000),
                        "quantity": random.randint(1, 100),
                        "remark": "测试包裹备注:" + GBK2312(5)})
    yubao_url = '/parcel/parcel/forecastParcel'
    yubao_params = {
        "operationPlatform": 2,
        "parcel": parcels
    }
        yubao_result = requests.post(wx_domain_test + yubao_url, headers=wx_header, json=yubao_params)
    print('预报包裹------------', tracking_number_list, json.loads(yubao_result.text)['message'])
    if json.loads(yubao_result.text)['message'] != 'ok':
        return 'yubao_error'
    return tracking_number_list


def storage_parcel(tracking_number_list):
    global parcel_id_list, parcel_code_list, parcel_list
    for tracking_number in tracking_number_list:
        shouhuo_url = '/crets-api/parcel/parcelReceiveWeight/saveParcelPhoto'
        shouhuo_params = {
            "headPath": "https://whalebird-parcel-image.oss-us-west-1.aliyuncs.com/file/parcelHead/2021/06/09/MB000013605.jpg",
            "image64data": "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",
            "invalidFlag": "1",
            "ocrJson": "",
            "ocrTime": 0,
            "receiveWeight": 0,
            "trackingNumber": tracking_number,
            "userIdentityCode": ""
        }
        # shouhuo_result = requests.post(yw_domain_test + shouhuo_url, headers=yw_header, json=shouhuo_params)
        # print('收货台收货-----------------', json.loads(shouhuo_result.text)['message'])
        # continue

        scan_url = '/crets-api/parcel/parcelUnpackingService/scanTrackingNumber'
        scan_params = {
            "trackingNumber": tracking_number,
            "warehouseId": "",
            "trackingNumberp": ""
        }
        scan_result = requests.get(yw_domain_test + scan_url, headers=yw_header, params=scan_params)
        parcel_code = json.loads(scan_result.text)['data'][0]['parcelCode']
        parcel_code_list.append(parcel_code)
        parcel_id = json.loads(scan_result.text)['data'][0]['parcelId']
        parcel_id_list.append(parcel_id)
        parcel_list.append({"parcelCode": parcel_code, "parcelId": parcel_id})
        parcel_detail_id = json.loads(scan_result.text)['data'][0]['parcelDetailId']
        print('包裹扫描-----------------', json.loads(scan_result.text)['message'])

        yanhuo_url = '/crets-api/parcel/parcelUnpackingService/updateParcelType'
        yanhuo_params = {
            "parcelId": parcel_id,
            "parcelInspectionProductType": "772068368839741440",
            "warehouseId": "21654",
            "parcelDetailId": parcel_detail_id,
            "unboxingFlag": "0",
            "volumnRatio": "100%"
        }
        yanhuo_result = requests.post(yw_domain_test + yanhuo_url, headers=yw_header, json=yanhuo_params)
        print('包裹验货-----------------', json.loads(yanhuo_result.text)['message'])

        uploadimage_url = '/crets-api/parcel/parcelReceiveWeight/uploadParcelImage'
        uploadimage_params = {
            "imagePath": "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",
            "imageType": 1,
            "parcelId": parcel_id
        }
        for i in range(3):
            uploadimage_result = requests.post(yw_domain_test + uploadimage_url, headers=yw_header,
                                               json=uploadimage_params)
            print('上传图片-----------------', json.loads(uploadimage_result.text)['message'])

        liangfang_url = '/crets-api/parcel/parcelUnpackingService/updateParcelMeasure'
        liangfang_params = {
            "parcelId": parcel_id,
            "parcelInspectionWeight": random.uniform(0.001, 2),
            "packageInspectionLength": random.randint(30, 50),
            "packageInspectionWidth": random.randint(15, 30),
            "packageInspectionHeight": random.randint(1, 15),
            "parcelDetailId": parcel_detail_id,
            "packageInspectionByManual": "1"
        }
        liangfang_result = requests.post(yw_domain_test + liangfang_url, headers=yw_header, json=liangfang_params)
        print('包裹量方-----------------', json.loads(liangfang_result.text)['message'])

        shangjia_url = '/crets-api/parcel/parcelUnpackingService/scanByPda'
        shangjia_params = {
            "warehouseId": "21654",
            "parcelCode": parcel_code,
            "type": 0,
            "onselfCargoSpaceCode": "HW-TS-{s1}-{s2}".format(s1=random.randint(1, 99), s2=random.randint(1, 99)),
            "parcelId": parcel_id
        }
        shangjia_result = requests.post(yw_domain_test + shangjia_url, headers=yw_header, json=shangjia_params)
        print('包裹上架-----------------', json.loads(shangjia_result.text)['message'])


def order_yundan(parcel_list):
    global parcel_group_id_list
    fangan_url = '/parcel/parcelSend/calculateScheme'
    fangan_params = {
        "activityType": "0",
        "addressId": "1054408895637884928",
        "isAirParcel": False,
        "pageNum": 1,
        "pageSize": 10,
        "parcelIdList": parcel_id_list
    }
    fangan_result = requests.post(wx_domain_test + fangan_url, headers=wx_header, params=fangan_params)
    shippingMethodId = json.loads(fangan_result.text)['data']['schemeRespVoList'][0]['shippingMethodId']
    schemeFee = json.loads(fangan_result.text)['data']['schemeRespVoList'][0]['schemeFee']

    print('直邮计算方案-----------------', json.loads(fangan_result.text)['message'])

    yundan_data_url = '/parcel/parcelSend/queryYundanSettelData'
    yundan_data_params = {
        "groupCountryCode": "US",
        "postCode": "12880",
        "schemeId": shippingMethodId,
        "totalMoney": schemeFee,
    }
    yundan_data_result = requests.post(wx_domain_test + yundan_data_url, headers=wx_header, params=yundan_data_params)
    yundan_data_datail = json.loads(yundan_data_result.text)['data']
    atttachmentFee = yundan_data_datail['atttachmentFee']  #超长超重附加费
    goodsFee = yundan_data_datail['goodsFee']  #消费税门槛
    consumptionTax = yundan_data_datail['consumptionTax']  #消费税比例
    discount = yundan_data_datail['discount']  #会员折扣
    totalDeclareFee = yundan_data_datail['totalDeclareFee']  #报关费
    totalMaterialFee = yundan_data_datail['totalMaterialFee']  #材料费
    totalShippingAttachmentFee = yundan_data_datail['totalShippingAttachmentFee']  #邮路附加费
    fee = yundan_data_datail['schemeLineRespVoList'][0]['fee']  #包裹运费
    boxVolumnWeight = yundan_data_datail['schemeLineRespVoList'][0]['boxVolumnWeight']  #预估货箱体积重
    boxWeight = yundan_data_datail['schemeLineRespVoList'][0]['boxWeight']  #预估货箱实重
    chargeWeight = yundan_data_datail['schemeLineRespVoList'][0]['chargeWeight']  #计费重
    remoteAttachmentFee = yundan_data_datail['schemeLineRespVoList'][0]['remoteAttachmentFee']  #偏远地区附加费
    deductionAmount = yundan_data_datail['schemeLineRespVoList'][0]['deductionAmount']  #体积豆抵扣金额
    totalVolumnBeanCnt = yundan_data_datail['totalVolumnBeanCnt']  #使用体积豆
    boxnum = math.ceil(chargeWeight / 15)

    print('直邮方案详情-----------------', json.loads(yundan_data_result.text)['message'])

    create_group_url = '/parcel/parcelSend/createParcelGroup'
    create_group_params = {
        "addressId": "1051860372602097664",
        "schemeId": shippingMethodId
    }
    create_group_result = requests.post(wx_domain_test + create_group_url, headers=wx_header,
                                        params=create_group_params)
    groupCode = json.loads(create_group_result.text)['data']['groupCode']
    parcelGroupId = json.loads(create_group_result.text)['data']['parcelGroupId']
    parcel_group_id_list.append(parcelGroupId)
    group_parcels[parcelGroupId] = {"parcel_list": parcel_list, "groupCode": groupCode, 'boxnum': boxnum}
    print('创建运单-----------------', groupCode, json.loads(create_group_result.text)['message'])

    goodsFee = 0 if goodsFee is None else goodsFee
    input_goodsFee = 1000  #输入商品价值计算消费税
    consumptionTaxFee = 0
    if consumptionTax is not None:
        consumptionTaxFee = round(input_goodsFee * consumptionTax / 100, 2) if input_goodsFee >= goodsFee else 0

    totalDiscountFee_after = fee - deductionAmount
    discountFee = round(totalDiscountFee_after * (1 - discount), 2)  #会员折扣金额
    totalFee = fee - discountFee - deductionAmount \
               + consumptionTaxFee \
               + atttachmentFee \
               + totalDeclareFee \
               + totalMaterialFee \
               + totalShippingAttachmentFee \
               + remoteAttachmentFee
    create_order_url = '/crets-order/order/generateOrder'
    create_order_params = {
        "consumptionTaxFee": consumptionTaxFee,
        "couponReqVo": {
            "discountFee": 0,
            "userCouponIdList": []},
        "discount": discount,
        "discountFee": discountFee,
        "goodsFee": input_goodsFee,
        "parcelGroupReqVoList": [{
            "chargeServiceReqVoList": [],
            "declareFee": totalDeclareFee,
            "deductionAmount": deductionAmount,
            "insuranceReqVoList": [],
            "orderParcelGroupBoxVoList": [{
                "boxHeight": 38,
                "boxLength": 58,
                "boxName": "HX01",
                "boxOutHeight": 40,
                "boxOutLength": 60,
                "boxOutWidth": 50,
                "boxSelfWeight": 1.5,
                "boxThick": "<Undefined>",
                "boxVolumeWeight": boxVolumnWeight,
                "boxWeight": boxWeight,
                "boxWidth": 48}],
            "parcelGroupId": parcelGroupId,
            "parcelReqVoList": parcel_list,
            "remoteAttachmentFee": remoteAttachmentFee,
            "shippingAttachmentFee": totalShippingAttachmentFee,
            "volumnBean": totalVolumnBeanCnt}],
        "parcelInfo": {
            "delayTotalFee": 0,
            "parcelList": []},
        "specialFee": 0,
        "specialWeight": 0,
        "totalAmount": fee,
        "totalAttachmentFee": atttachmentFee,
        "totalChargeServiceFee": 0,
        "totalDeclareFee": totalDeclareFee,
        "totalDeductionAmount": deductionAmount,
        "totalDiscountFee": 0,
        "totalFee": totalFee,
        "totalInsuranceFee": 0,
        "totalMaterialFee": totalMaterialFee,
        "totalShippingAttachmentFee": totalShippingAttachmentFee,
        "totalVolumnBean": totalVolumnBeanCnt
    }
    create_order_result = requests.post(wx_domain_test+ create_order_url, headers=wx_header,
                                        json=create_order_params)
    pay_order_id = json.loads(create_order_result.text)['data']
    print('创建订单-----------------', json.loads(create_order_result.text)['message'])
    if json.loads(create_order_result.text)['message'] != 'ok':
        return 'error'

    banlance_pay_url = '/crets-order/order/balancePay'
    banlance_pay_params = {
        "payOrderId": pay_order_id
    }
    banlance_pay_result = requests.post(wx_domain_test + banlance_pay_url, headers=wx_header,
                                        params=banlance_pay_params)
    if json.loads(banlance_pay_result.text)['message'] == '余额不足':
        print('余额支付-----------------', json.loads(banlance_pay_result.text)['message'])
        return 'error'
    print('余额支付-----------------', json.loads(banlance_pay_result.text)['message'])


def warehouse_operation(parcelGroupIds, group_parcels):
    print_sort_url = '/crets-api/parcel/printSort/printSort'
    print_sort_params = {
        "parcelGroupIds":
            parcel_group_id_list,
        "isAll": "0",
        "warehouseId": "21654",
        "printStatus": "0"
    }
    print_sort_result = requests.post(yw_domain_test + print_sort_url, headers=yw_header,
                                      json=print_sort_params)
    print('打印拣货单-----------------', print_sort_result.status_code)
    for parcelGroupId in parcelGroupIds:
        for group_parcel in group_parcels[parcelGroupId]['parcel_list']:
            sort_checking_url = '/crets-api/parcel/sortChecking/scanParcel'
            sort_checking_params = {
                "warehouseId": 21654,
                "parcelCode": group_parcel['parcelCode'],
                "parcelGroupId": parcelGroupId
            }
            sort_checking_result = requests.get(yw_domain_test + sort_checking_url, headers=yw_header,
                                                params=sort_checking_params)
            print('包裹核验-----------------', sort_checking_result.status_code)
        finsh_checking_url = '/crets-api/parcel/sortChecking/finishCheck'
        finsh_checking_params = {
            "parcelGroupId": parcelGroupId
        }
        finsh_checking_result = requests.get(yw_domain_test + finsh_checking_url, headers=yw_header,
                                             params=finsh_checking_params)
        print('完成核验-----------------', finsh_checking_result.status_code)

        #包裹随机装箱
        boxlist = []
        parcellist = group_parcels[parcelGroupId]['parcel_list']
        boxnum = group_parcels[parcelGroupId]['boxnum']
        boxparcel_num = int(len(parcellist) / boxnum)
        boxparcel_list = []
        for i in range(0, len(parcellist), boxparcel_num):
            boxparcel_list.append(parcellist[i:i + boxparcel_num])
        print(boxparcel_list)
        for index, boxparcels in enumerate(boxparcel_list):
            boxCode = group_parcels[parcelGroupId]['groupCode'] + '-0' + str(index + 1)
            scan_boxcode_url = '/crets-api/parcel/parcelPacking/scanBoxCode'
            scan_boxcode_params = {
                "boxCode": boxCode
            }
            scan_boxcode_result = requests.post(yw_domain_test + scan_boxcode_url, headers=yw_header,
                                                params=scan_boxcode_params)
            print('扫描货箱-----------------', json.loads(scan_boxcode_result.text)['message'])
            for boxparcel in boxparcels:
                scan_box_parcelcode_url = '/crets-api/parcel/parcelPacking/saveBoxAndParcel'
                scan_box_parcelcode_params = {
                    "boxCode": boxCode,
                    "parcelCode": boxparcel['parcelCode']
                }
                scan_box_parcelcode_result = requests.post(yw_domain_test + scan_box_parcelcode_url, headers=yw_header,
                                                           params=scan_box_parcelcode_params)
                print('包裹关联货箱-----------------', json.loads(scan_box_parcelcode_result.text)['message'])
            boxlist.append({
                "boxCode": boxCode,
                "boxWeight": random.uniform(10, 20),
                "boxHeight": random.randint(40, 60),
                "boxLength": random.randint(20, 40),
                "boxWidth": random.randint(1, 20),
                "declareList": [
                    {
                        "declareCnName": "测试",
                        "declareEnName": "test",
                        "declarePrice": "100",
                        "hsCode": "100",
                        "material": "100",
                        "purpose": "100",
                        "quantity": "100"
                    }
                ]
            })

        finish_box_url = '/crets-api/parcel/parcelPacking/finishBoxConfirm'
        finish_box_params = {
            "parcelGroupId": parcelGroupId,
            "list": boxlist,
            "packingNum": len(boxlist)
        }
        finish_box_result = requests.post(yw_domain_test + finish_box_url, headers=yw_header,
                                          json=finish_box_params)
        print('完成装箱-----------------', json.loads(finish_box_result.text)['message'])


tasknum = 1  #运单数
start_num = 0
parcel_group_id_list = []
group_parcels = {}
for i in range(tasknum):
    parcel_code_list = []
    parcel_id_list = []
    parcel_list = []
    # parcelnum = random.randint(10,20) #运单内包裹数
    parcelnum = 30  #运单内包裹数
    tracking_number_list = create_parcel(parcelnum)
    if tracking_number_list == 'yubao_error':
        break
    storage_parcel(tracking_number_list)
    order_message = order_yundan(parcel_list)
    if order_message == 'error':
        break
    warehouse_operation(parcel_group_id_list, group_parcels)
