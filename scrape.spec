# -*- mode: python -*-

block_cipher = None


a = Analysis(['scrape.py'],
             pathex=['C:\\Users\\Atulya\\Documents\\GitHub\\news-sentiment-analysis'],
             binaries=[],
             datas=[
             ('.\\news_spider\\*.py','news_spider'),
             ('.\\news_spider\\spiders\\*.py','news_spider\\spiders'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\*.py','scrapy'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\spidermiddlewares\\*.py','scrapy\\spidermiddlewares'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\pipelines\\*.py','scrapy\\pipelines'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\selector\\*.py','scrapy\\selector'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\loader\\*.py','scrapy\\loader'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\commands\\*.py','scrapy\\commands'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\contracts\\*.py','scrapy\\contracts'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\settings\\*.py','scrapy\\settings'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\spiders\\*.py','scrapy\\spiders'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\utils\\*.py','scrapy\\utils'),
             ('C:\\Users\\Atulya\\Anaconda3\\Lib\\site-packages\\scrapy\\xlib\\*.py','scrapy\\xlib'),
             ('C:\\Users\\Atulya\\Anaconda3\\envs\\news-sentiment-analysis\\Lib\\site-packages\\rotating_proxies\\*py','rotating_proxies'),          
             ],
             hiddenimports=[
             'urllib.request',
             'queuelib', 
             'scrapy.spiderloader',
             'news_spider.spiders',
             'news_spider.settings',
             'news_spider.items',
             'news_spider.middlewares',
             'news_spider.pipelines',
             'news_spider.spiders.economictimes',
             'news_spider.spiders.moneycontrol',
             'pandas',
             'nsepy',
             'scrapy',
             'scrapy.core',
             'scrapy.core.downloader',
             'scrapy.core.scheduler',
             'scrape.core.engine',
             'scrape.core.scraper',
             'scrape.core.spidermw',
             'scrapy.statscollectors',
             'scrapy.logformatter',
             'scrapy.extensions',
             'scrapy.extensions.corestats',
             'scrapy.extensions.telnet',
             'scrapy.extensions.memusage',
             'scrapy.extensions.closespider',
             'scrapy.extensions.debug',
             'scrapy.extensions.feedexport',
             'scrapy.extensions.httpcache',
             'scrapy.extensions.logstats',
             'scrapy.extensions.memdebug',
             'scrapy.extensions.spiderstate',
             'scrapy.extensions.throttle',
             'scrapy.extensions.statsmailer',
             'scrapy.downloadermiddlewares',
             'scrapy.core.downloader.handlers.ftp',
             'scrapy.core.downloader.handlers.http',
             'scrapy.core.downloader.handlers.datauri',
             'scrapy.core.downloader.handlers.file',
             'scrapy.core.downloader.handlers.s3',
             'scrapy.core.downloader.contextfactory',
             'scrapy.downloadermiddlewares.defaultheaders',
             'scrapy.downloadermiddlewares.useragent',
             'scrapy.downloadermiddlewares.stats',
             'scrapy.downloadermiddlewares.retry',
             'scrapy.downloadermiddlewares.robotstxt',
             'scrapy.downloadermiddlewares.httpauth',
             'scrapy.downloadermiddlewares.downloadtimeout',
             'scrapy.downloadermiddlewares.redirect',
             'scrapy.downloadermiddlewares.httpproxy',
             'scrapy.downloadermiddlewares.httpcompression',
             'scrapy.downloadermiddlewares.httpcache',
             'scrapy.downloadermiddlewares.decompression',
             'scrapy.downloadermiddlewares.cookies',
             'scrapy.downloadermiddlewares.chunked',
             'scrapy.downloadermiddlewares.ajaxcrawl'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='News Scraper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='C:\\Users\\Atulya\\Documents\\GitHub\\news-sentiment-analysis\\scrape.ico' )
