<?php
function Ip($type = 0) 
{
            $type = $type ? 1 : 0;
            static $ip =  NULL;
            if ($ip !== NULL) return $ip[$type];
            if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
                $arr = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
                $pos = array_search('unknown',$arr);
                if(false !== $pos) unset($arr[$pos]);
                $ip = trim($arr[0]);
            }elseif (isset($_SERVER['HTTP_CLIENT_IP'])) {
                $ip = $_SERVER['HTTP_CLIENT_IP'];
            }elseif (isset($_SERVER['REMOTE_ADDR'])) {
                $ip = $_SERVER['REMOTE_ADDR'];
            }
            $long = sprintf("%u",ip2long($ip));
            $ip = $long ? array($ip, $long) : array('0.0.0.0', 0);
            return $ip[$type];
        }

if(!isset($_POST['submit'])){
	exit('非法访问!');
}
$username = $_POST['username'];
$password = $_POST['password'];
//注册信息判断
if(!preg_match('/^[\w\x80-\xff]{3,15}$/', $username)){
	exit('错误：用户名不符合规定。<a href="javascript:history.back(-1);">返回</a>');
}
if(strlen($password) < 4){
	exit('错误：密码长度不符合规定。<a href="javascript:history.back(-1);">返回</a>');
}

//包含数据库连接文件
include('conn.php');
//检测用户名是否已经存在
$check_query = mysql_query("select AccountID from tbl_user where AccountID='$username'");
if(mysql_fetch_array($check_query)){
	echo '错误：用户名 ',$username,' 已存在。<a href="javascript:history.back(-1);">返回</a>';
	exit;
}
//写入数据
//$password = MD5($password); //不使用MD5格式密码
//$regdate = time();
$ip = ip();
$sql = "INSERT INTO tbl_user(AccountID,AccountPassword,EnableFlg,TrialFlg,DownFlg,ExpFlg,SequenceNumber,UseFlg,BadMsg,CdKey)VALUES('$username','$password','1','8','0','0','13','1','0','$username')";
if(mysql_query($sql,$conn)){
	exit('用户注册成功！');
} else {
	echo '抱歉！添加数据失败：',mysql_error(),'<br />';
	echo '点击此处 <a href="javascript:history.back(-1);">返回</a> 重试';
}
?>
