import http.server
import socketserver
import urllib.parse
import wikipedia

# Konfigurasi Wikipedia
wikipedia.set_lang("id")

class WikipediaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        keyword = query_params.get('keyword', ['Python Programming'])[0]
        html_content = self.generate_html(keyword)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def get_long_article(self, keyword):
        """Ambil artikel yang lebih panjang dan detail"""
        try:
            # Method 1: Ambil summary dengan lebih banyak sentences
            summary = wikipedia.summary(keyword, sentences=25)
            return summary
            
        except:
            try:
                # Method 2: Ambil konten lengkap page
                page = wikipedia.page(keyword)
                full_content = page.content
                
                # Potong menjadi bagian yang lebih readable
                paragraphs = full_content.split('\n\n')
                meaningful_content = []
                char_count = 0
                
                for para in paragraphs:
                    if len(para) > 50:  # Hanya paragraph yang meaningful
                        meaningful_content.append(para)
                        char_count += len(para)
                        if char_count > 2500:  # Batasi total karakter
                            break
                
                return '\n\n'.join(meaningful_content)
                
            except:
                return f"Tidak dapat mengambil konten panjang untuk '{keyword}'"
    
    def generate_html(self, keyword):
        try:
            page = wikipedia.page(keyword)
            
            # AMBIL ARTIKEL LEBIH PANJANG - PILIH SALAH SATU:
            
            # Option A: Summary panjang (25 kalimat)
            summary = wikipedia.summary(keyword, sentences=25)
            
            # Option B: Konten custom yang lebih panjang
            # summary = self.get_long_article(keyword)
            
            # Option C: Multiple sections
            # summary = self.get_multiple_sections(keyword)
            
            related_articles = []
            try:
                search_results = wikipedia.search(keyword, results=15)
                for title in search_results:
                    try:
                        if title.lower() != keyword.lower():
                            related_summary = wikipedia.summary(title, sentences=2)  # Tambah jadi 2 kalimat
                            related_articles.append({
                                'title': title,
                                'summary': related_summary
                            })
                        if len(related_articles) >= 10:
                            break
                    except:
                        continue
            except:
                related_articles = []
            
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                page = wikipedia.page(e.options[0])
                summary = wikipedia.summary(e.options[0], sentences=25)  # Juga lebih panjang
                related_articles = []
            except:
                summary = f"Terjadi kesalahan saat mengambil artikel untuk '{keyword}'. Silakan coba kata kunci lain."
                related_articles = []
        except wikipedia.exceptions.PageError:
            summary = f"Tidak ditemukan artikel untuk '{keyword}'. Silakan coba kata kunci lain."
            related_articles = []
        except Exception as e:
            summary = f"Terjadi kesalahan: {str(e)}"
            related_articles = []

        # Escape HTML characters dan format lebih baik
        safe_summary = summary.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        safe_summary = safe_summary.replace('\n', '</p><p>')  # Convert newlines to paragraphs
        safe_keyword = keyword.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

        # Build HTML dengan layout yang mendukung konten panjang
        html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wikipedia Artikel Generator 2025 - {safe_keyword}</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --light-color: #ecf0f1;
            --dark-color: #2c3e50;
            --text-color: #333;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background-color: #f9f9f9;
            display: grid;
            grid-template-rows: auto 1fr auto;
            min-height: 100vh;
        }}
        
        .container {{
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px 0;
            text-align: center;
            box-shadow: var(--box-shadow);
        }}
        
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        nav {{
            background-color: white;
            padding: 15px 0;
            box-shadow: var(--box-shadow);
            margin-bottom: 30px;
        }}
        
        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .menu {{
            display: flex;
            list-style: none;
        }}
        
        .menu li {{
            margin-left: 25px;
        }}
        
        .menu a {{
            text-decoration: none;
            color: var(--dark-color);
            font-weight: 500;
            transition: color 0.3s;
            padding: 5px 10px;
            border-radius: var(--border-radius);
        }}
        
        .menu a:hover {{
            color: var(--secondary-color);
            background-color: var(--light-color);
        }}
        
        .search-container {{
            background-color: white;
            padding: 30px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            margin-bottom: 30px;
        }}
        
        .search-form {{
            display: flex;
            gap: 10px;
        }}
        
        .search-input {{
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            font-size: 1rem;
        }}
        
        .search-button {{
            background-color: var(--secondary-color);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: var(--border-radius);
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.3s;
        }}
        
        .search-button:hover {{
            background-color: #2980b9;
        }}
        
        .main-content {{
            background-color: white;
            padding: 40px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }}
        
        .article-title {{
            color: var(--primary-color);
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--light-color);
        }}
        
        .article-content {{
            line-height: 1.8;
            font-size: 1.1rem;
        }}
        
        .article-content p {{
            margin-bottom: 20px;
            text-align: justify;
        }}
        
        .article-content p:first-child {{
            font-size: 1.2rem;
            font-weight: 500;
            color: var(--primary-color);
        }}
        
        .article-stats {{
            background-color: var(--light-color);
            padding: 15px;
            border-radius: var(--border-radius);
            margin: 25px 0;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .sidebar {{
            background-color: white;
            padding: 25px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            height: fit-content;
            position: sticky;
            top: 20px;
        }}
        
        .sidebar-title {{
            color: var(--primary-color);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--light-color);
        }}
        
        .related-articles {{
            list-style: none;
        }}
        
        .related-articles li {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .related-articles a {{
            text-decoration: none;
            color: var(--secondary-color);
            font-weight: 500;
            display: block;
            transition: color 0.3s;
            margin-bottom: 5px;
        }}
        
        .related-articles a:hover {{
            color: var(--accent-color);
        }}
        
        .related-summary {{
            font-size: 0.85rem;
            color: #666;
            line-height: 1.4;
        }}
        
        footer {{
            background-color: var(--dark-color);
            color: white;
            text-align: center;
            padding: 25px 0;
            margin-top: 50px;
        }}
        
        .footer-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .current-keyword {{
            background-color: var(--light-color);
            padding: 15px 20px;
            border-radius: var(--border-radius);
            margin-bottom: 25px;
            font-weight: 500;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .article-length {{
            font-size: 0.9rem;
            color: #666;
            background: white;
            padding: 5px 10px;
            border-radius: 15px;
        }}
        
        @media (max-width: 992px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
            
            .nav-container {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .menu {{
                flex-wrap: wrap;
                justify-content: center;
            }}
            
            .menu li {{
                margin: 5px 10px;
            }}
            
            .main-content {{
                padding: 25px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Wikipedia Artikel Generator</h1>
        <p>Jelajahi pengetahuan dari seluruh dunia - 2025 Edition</p>
    </header>
    
    <nav>
        <div class="nav-container">
            <div class="logo">WikiExplorer</div>
            <ul class="menu">
                <li><a href="?keyword=Indonesia">Beranda</a></li>
                <li><a href="?keyword=Teknologi">Artikel Populer</a></li>
                <li><a href="?keyword=Sejarah">Kategori</a></li>
                <li><a href="?keyword=Python%20(programming%20language)">Programming</a></li>
                <li><a href="?keyword=Ilmu%20Pengetahuan">Sains</a></li>
            </ul>
        </div>
    </nav>
    
    <div class="container">
        <main>
            <div class="search-container">
                <form class="search-form" method="GET">
                    <input type="text" name="keyword" class="search-input" placeholder="Masukkan kata kunci artikel Wikipedia..." value="{safe_keyword}">
                    <button type="submit" class="search-button">Cari Artikel</button>
                </form>
            </div>
            
            <div class="main-content">
                <div class="current-keyword">
                    <span>Menampilkan hasil untuk: <strong>{safe_keyword}</strong></span>
                    <span class="article-length">{len(summary)} karakter</span>
                </div>
                <h2 class="article-title">📚 {safe_keyword}</h2>
                <div class="article-stats">
                    🔍 Artikel panjang dengan {summary.count('.')} kalimat | 
                    📖 {len(summary.split())} kata | 
                    ⏱️ Bacaan {max(1, len(summary.split()) // 200)} menit
                </div>
                <div class="article-content">
                    <p>{safe_summary}</p>
                </div>
            </div>
        </main>
        
        <aside class="sidebar">
            <h3 class="sidebar-title">🔗 Artikel Terkait</h3>
            <ul class="related-articles">"""

        # Add related articles
        for article in related_articles[:10]:
            safe_title = article['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            safe_article_summary = article['summary'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            html += f"""
                <li>
                    <a href="?keyword={urllib.parse.quote(article['title'])}">{safe_title}</a>
                    <div class="related-summary">{safe_article_summary[:120]}...</div>
                </li>"""

        if not related_articles:
            html += """
                <li style="color: #666; font-style: italic;">
                    Tidak ada artikel terkait yang ditemukan. Coba kata kunci lain.
                </li>"""

        html += """
            </ul>
            
            <div style="margin-top: 25px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <h4 style="color: var(--primary-color); margin-bottom: 10px;">💡 Tips</h4>
                <p style="font-size: 0.85rem; color: #666; line-height: 1.4;">
                    Gunakan kata kunci spesifik untuk artikel yang lebih panjang dan detail.
                </p>
            </div>
        </aside>
    </div>
    
    <footer>
        <div class="footer-content">
            <p>&copy; 2025 Wikipedia Artikel Generator. Semua hak dilindungi undang-undang.</p>
            <p>Dibuat dengan Python dan Wikipedia API | Konten dari Wikimedia Foundation</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), WikipediaHandler) as httpd:
        print(f"🚀 Server berjalan di http://localhost:{PORT}")
        print("📍 Contoh: http://localhost:8000/?keyword=Indonesia")
        print("📍 Contoh: http://localhost:8000/?keyword=Sejarah%20Indonesia")
        print("⏹️  Tekan Ctrl+C untuk menghentikan server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server dihentikan")
