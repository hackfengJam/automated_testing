#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
__Date__ = "2018/3/16 下午6:08"

# from ecams.utils.exceptions import except_dict

# for key in except_dict:
#     if 'error_message' in except_dict[key]:
#         '# http_code:', except_dict[key].get('http_code', ''), 'error_message:', except_dict[key].get('error_message',
#                                                                                                       '')
#         continue
#     else:
#         print '#', except_dict[key].get('message', '')
#     print key, '=', except_dict[key]['code']
#     print

SUCCESS = 0
# Access Key Exists
AkExists = 202004

# Access Key Get Policies Error
AkPoliciesError = 202005

# Token is invalid
InvalidToken = 202009

# access token is expired
AcceessTokenExpired = 207004

# verify code error
VerifyCodeError = 204002

# Primary Access Key Not Allow
PrimaryAkNotAllow = 202003

# Insufficient quota
AkInsufficientQuota = 202010

# MessageNotFound
MessageNotFound = 204001

# Sync Resource Error
SyncResourceError = 202008

# Sub User Quota Exceeded
SubUserQuotaExceeded = 201010

# Sub User Not Found
SubUserNotFound = 201007

# third party account verify failed
ThirdPartyAccountVerifyFailed = 207001

# User Not Found
UserNotFound = 201004

# cloud account not found
CloudAccountNotFound = 208001

# NeedLogin
NeedLogin = 101002

# this token is not belong to you
TokenNotFound = 205001

# access token doesn't exists
AccessTokenNotExists = 207002

# View Not Found
ViewNotFound = 201011

# Bad Request.
BadRequest = 206002

# Primary Account Not Found
PrimaryAccountNotFound = 201008

# Primary Account Locked
PrimaryAccountLocked = 201009

# account not found
AccountNotFound = 207006

# parameter error: {info}
ParamsError = 206001

# Permission Not Found
PermissionNotFound = 201013

# Username Exists
UsernameExists = 201006

# Not Permission
NotPermission = 201012

# token count is exceeded
TokenExceeded = 205003

# CloudCare Error
CloudCareError = 208003

# SSO Error
SSOError = 208004

# invalid access token
InvalidAcceessToken = 207005

# Need Primary Account
NeedPrimaryAccount = 201003

# consume record not found
ConsumeRecordNotFound = 208002

# Password Error
PasswordError = 201005

# Access Key AccountId Error
AkAccountIdError = 202007

# refresh token doesn't exists
RefreshTokenNotExists = 207003

# Invalid Parameter.
InvalidParameter = 206003

# Access Key Get Policies Error
AkPoliciesReadOnlyError = 202006

# this token is not belong to you
TokenNotBelongToYou = 205002

# Access Key Error
AkError = 202002

# verify code expired
VerifyCodeExpired = 204003

# LoginFailed
LoginFailed = 201001
