import email
import imaplib
import re

# 163邮箱设置   yll708854084@163.com
username = "yll708854084@163.com"  # 替换为你的邮箱用户名 yll70_wfmgw3n3tb@aka.yeah.net
password = "NSJYHILIOURLMBDR"          # 替换为你的密码    NSJYHILIOURLMBDR
imap_url = "imap.163.com"           # 163邮箱的IMAP服务器地址

# 连接到IMAP服务器
imaplib.Commands['ID'] = ('AUTH')

conn = imaplib.IMAP4_SSL(host = imap_url, port='993')
conn.login(username, password)

# 准备IMAP ID信息并格式化为合适的字符串形式
imap_id_info = '("name" "myname" "version" "1.0.0" "vendor" "MyVendor" "support-email" "support@example.com")'
# 发送IMAP ID命令
conn._simple_command('ID', imap_id_info)

result, data = conn.select("inbox")



# 搜索未读邮件
status, messages = conn.search(None, 'UNSEEN')

# 获取最新的邮件
messages = messages[0].split(b' ')
latest_email_id = messages[-1]

# 获取邮件内容
_, msg = conn.fetch(latest_email_id, '(RFC822)')
msg = email.message_from_bytes(msg[0][1])

# 遍历邮件内容
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode()
            # 使用正则表达式从邮件正文中提取验证码
            verification_code = re.search(r'\d{4,6}', body)
            if verification_code:
                verification_code = verification_code.group(0)
                print("Verification Code:", verification_code)
else:
    body = msg.get_payload(decode=True).decode()
    # 提取验证码
    verification_code = re.search(r'\d{4,6}', body)
    if verification_code:
        verification_code = verification_code.group(0)
        print("Verification Code:", verification_code)

# 关闭连接
conn.close()
conn.logout()
