import time
import yt_dlp
import os
import sys

# 配置常量
DOWNLOAD_DIR = "D:/Taylor/Downloads/Video"
BROWSER_COOKIES = 'firefox'
FFMPEG_PATH = os.path.join("ffmpeg", "ffmpeg.exe")  # 更加健壮的路径连接


def clear_screen():
    """清除终端屏幕，支持 Windows 和其他系统"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ffmpeg_path():
    """获取 ffmpeg 的路径"""
    if getattr(sys, 'frozen', False):  # 如果是打包后的环境
        return os.path.join(sys._MEIPASS, "ffmpeg", "ffmpeg.exe")
    return os.path.join("ffmpeg", "ffmpeg.exe")  # 调试模式

def configure_yt_dlp_options(url, output_path=DOWNLOAD_DIR, cookies=BROWSER_COOKIES):
    """配置 yt-dlp 参数"""
    return {
        'format': 'bestvideo+bestaudio/best',  # 下载最佳视频质量
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # 设置输出文件名和路径
        'ffmpeg_location': FFMPEG_PATH,  # 指定 ffmpeg 路径
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # 转换视频格式为 mp4
        }],
        'quiet': False,  # 显示下载进度
        'cookiesfrombrowser': (cookies,) if "bilibili" in url else None,  # 如果是 Bilibili 使用浏览器 cookies
    }


def download_video(url, cookies=BROWSER_COOKIES, output_path=DOWNLOAD_DIR):
    """下载视频并处理错误"""
    ydl_opts = configure_yt_dlp_options(url, output_path, cookies)

    # 使用 yt-dlp 下载视频
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("正在获取视频信息...")
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            video_duration = round(info_dict.get('duration', 0))  # 获取视频长度，单位秒
            video_resolution = [info_dict.get('width', 'Unknown resolution'), info_dict.get('height', 'Unknown resolution')]  # 获取视频的分辨率高度（若没有，默认 'Unknown resolution'）
            uploader = info_dict.get('uploader', 'Unknown uploader')  # 获取上传者的名称

            # 打印视频信息
            print(f"视频标题：{video_title}")
            print(f"上传者：{uploader}")
            print(f"视频时长：{video_duration // 60} 分 {video_duration % 60} 秒")
            print(f"分辨率：{video_resolution[0]}p * {video_resolution[1]}p")  # 假设视频的分辨率高度就是 `height` 字段

            print("开始下载...")
            ydl.download([url])
            print(f"{video_title} 下载完成！")
    except yt_dlp.DownloadError as e:
        print(f"下载失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    FFMPEG_PATH = get_ffmpeg_path()
    while True:
        video_url = input("请输入要下载的视频链接：\n")
        if video_url.strip():
            download_video(video_url)
        else:
            print("无效的链接，请重新输入。")

        user_input = input("\n按 'q' 退出程序，或按任意键重新开始: ").strip().lower()
        if user_input == 'q':
            print("程序退出。再见！")
            time.sleep(3)
            break  # 退出循环，结束程序
        else:
            clear_screen()
            print("程序重启中...\n")
