# 🚀 QUICK SETUP & DEPLOYMENT GUIDE

> Get your quantum mechanics animations live on GitHub Pages in 30 minutes!

## 📋 Prerequisites

- GitHub account (free)
- Git installed
- Python 3.12+
- Figma account (optional, for custom UI)

## ⚡ 30-Minute Setup

### Step 1: Optimize Project (2 min)
```bash
cd /workspaces/animation_quantum_mech_basics
bash scripts/optimize_project.sh
```
✅ Consolidates documentation, removes duplicates, saves space

### Step 2: Create GitHub Repository (3 min)
1. Go to https://github.com/new
2. Name: `animation_quantum_mech_basics`
3. Description: "Quantum Mechanics Interactive Simulator"
4. **Public** repository
5. Click "Create repository"

### Step 3: Setup Git & Push (5 min)
```bash
cd /workspaces/animation_quantum_mech_basics

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize and push
git init
git add .
git commit -m "Initial commit: Quantum mechanics animation pipeline"
git remote add origin https://github.com/YOUR_USERNAME/animation_quantum_mech_basics.git
git branch -M main
git push -u origin main
```

### Step 4: Create GitHub Pages Site (10 min)
```bash
bash scripts/deploy_github_pages.sh
```

This creates:
- `docs/index.html` - Website home page
- `docs/style.css` - Styling
- `docs/script.js` - Interactivity
- `_config.yml` - Jekyll configuration
- `.gitignore` - Exclude large files
- `README.md` - Quick reference

### Step 5: Enable GitHub Pages (3 min)
1. Go to your repository on GitHub
2. Settings → Pages
3. Source: **Deploy from branch**
4. Branch: **main**
5. Folder: **/docs**
6. Click **Save**

### Step 6: Verify Deployment (2 min)
```bash
git add .
git commit -m "Deploy GitHub Pages"
git push origin main

# Wait 1-2 minutes for GitHub to build
# Visit: https://YOUR_USERNAME.github.io/animation_quantum_mech_basics
```

✅ **Website is now live!**

---

## 🎬 Adding Animations to Your Website

### Quick Preview (5 minutes)
```bash
# Render one animation (low quality)
pip install manim
manim -ql src/manim_quantum.py HarmonicOscillatorScene

# This creates: videos/1080p60/HarmonicOscillatorScene.mp4
```

### Production Quality (30+ minutes)
```bash
# Render all 4 animations (high quality)
manim -qh src/manim_quantum.py HarmonicOscillatorScene
manim -qh src/manim_quantum.py InfiniteWellScene
manim -qh src/manim_quantum.py FiniteWellScene
manim -qh src/manim_quantum.py TunnelingScene

# Encode to 4K MP4
python3 << 'PYTHON'
from src.ffmpeg_pipeline import QuantumAnimationPipeline
p = QuantumAnimationPipeline()
for scene in ['HarmonicOscillator', 'InfiniteWell', 'FiniteWell', 'Tunneling']:
    input_mp4 = f'videos/1080p60/{scene}Scene.mp4'
    output_4k = f'docs/animations/{scene}_4K.mp4'
    print(f"Encoding {scene}...")
    p.mp4_encode_4k(input_mp4, output_4k)
PYTHON
```

### Update Website
```bash
# Copy animation MP4s to docs/animations/
mkdir -p docs/animations
cp outputs/*.mp4 docs/animations/
cp outputs/*.gif docs/animations/

# Push to GitHub
git add docs/animations
git commit -m "Add quantum animation videos"
git push origin main

# Website updates automatically!
```

---

## 🎨 Adding Figma Design (Optional - 10 minutes)

### Step 1: Create Figma Design
1. Go to https://figma.com
2. Create new file: "Quantum Mechanics UI"
3. Design your interface:
   - Control panels
   - Visualization areas
   - Navigation
   - Footer

### Step 2: Get Figma Credentials
1. Click **Share** → Get link
2. Extract file key: `figma.com/design/[FILE_KEY]/...`
3. Settings → Developer → Create personal access token
4. Copy token

### Step 3: Generate Web Components
```bash
python3 scripts/figma_connector.py \
  --file-key YOUR_FILE_KEY \
  --token YOUR_TOKEN \
  --output docs/components

# Or use environment variables
export FIGMA_FILE_KEY="YOUR_FILE_KEY"
export FIGMA_TOKEN="YOUR_TOKEN"
python3 scripts/figma_connector.py
```

### Step 4: Update Website
```bash
# Components are generated in docs/components/
# Push to GitHub
git add docs/components
git commit -m "Add Figma-designed UI components"
git push origin main

# Visit website - UI is now live!
```

---

## 📊 What You'll Have After Setup

### ✅ Website Features
- 🏠 Home page with overview
- 🎬 Animation gallery (video player)
- 📚 Documentation links
- 🎮 Link to interactive notebook
- 🎨 Figma-designed components (optional)
- 📱 Mobile responsive
- ⚡ Fast loading (hosted on GitHub Pages)

### ✅ GitHub Pages Components
```
docs/
├── index.html          ← Website home
├── style.css           ← Styling
├── script.js           ← Interactivity
├── animations/         ← MP4 videos
├── components/         ← Figma components (optional)
└── assets/             ← Images, icons, etc.
```

---

## 🔗 Website URLs

```
Main site:     https://YOUR_USERNAME.github.io/animation_quantum_mech_basics
Documentation: https://github.com/YOUR_USERNAME/animation_quantum_mech_basics/blob/main/COMPREHENSIVE_README.md
Source code:   https://github.com/YOUR_USERNAME/animation_quantum_mech_basics
```

---

## 📱 Mobile Responsive

Website automatically works on:
- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)

---

## 🚀 Advanced: Custom Domain (Optional)

To use your own domain (like `quantum.yoursite.com`):

1. Buy domain from any registrar
2. GitHub Settings → Pages
3. Add custom domain
4. Follow DNS setup instructions
5. Website is now at your custom domain!

---

## 🐛 Troubleshooting

### Website Not Appearing
- Check GitHub Pages is enabled (Settings → Pages)
- Wait 2-3 minutes for build
- Check Actions tab for build errors
- Ensure `/docs` folder contains `index.html`

### Animations Not Playing
- Ensure MP4 files are in `docs/animations/`
- Check file paths in HTML
- Verify files are pushed to GitHub (`git push`)
- Refresh browser cache (Ctrl+Shift+Del)

### Figma Connection Failed
- Verify token is correct
- Check file key is valid
- Ensure token has read permissions
- Try: `python3 scripts/figma_connector.py --test`

### Large File Upload Fails
- GitHub has file size limits (~100 MB)
- Split videos or use lower bitrate
- Use `.gitignore` to exclude large files
- Consider GitHub Releases for large files

---

## 📈 Performance Tips

### Optimize Videos
```bash
# Smaller file size with lower bitrate
python3 << 'PYTHON'
from src.ffmpeg_pipeline import QuantumAnimationPipeline
p = QuantumAnimationPipeline()
# Use lower bitrate (default 50M)
p.mp4_encode_4k('input.mp4', 'output.mp4', bitrate='10M')
PYTHON
```

### Compress Images
```bash
# Reduce PNG sizes
for file in outputs/*.png; do
  optipng -o2 "$file"
done
```

### Use CDN for Videos (Advanced)
- Upload videos to Cloudinary
- Embed from CDN instead of GitHub
- Much faster loading!

---

## 📝 File Consolidation Results

| Before | After | Saved |
|--------|-------|-------|
| 17 markdown files | 1 comprehensive + quick ref | ~150 KB |
| 4 debug scripts | Removed | ~20 KB |
| 1 old notebook | Removed | ~14 KB |
| .venv included | Git excluded | ~500 MB |
| **Total**: ~1 GB | **New**: ~50 MB | **~950 MB!** |

---

## ✅ Final Checklist

Before sharing your website:

- [ ] Repository created on GitHub
- [ ] GitHub Pages enabled
- [ ] Website accessible at GitHub URL
- [ ] COMPREHENSIVE_README.md is comprehensive
- [ ] README.md is clear and helpful
- [ ] All animations uploaded (optional)
- [ ] Figma UI integrated (optional)
- [ ] `.gitignore` configured properly
- [ ] Website tested on mobile
- [ ] Shared with collaborators!

---

## 🎓 What Visitors Will See

### Website Highlights
1. **Home Page**
   - Project title and description
   - Feature overview
   - Quick links

2. **Animation Gallery**
   - 4 quantum system animations
   - Video player with controls
   - Descriptions for each

3. **Interactive Simulator**
   - Instructions to run locally
   - Link to Jupyter notebook
   - Quick setup commands

4. **Documentation**
   - COMPREHENSIVE_README.md
   - Quick start guide
   - GitHub repository link

5. **Footer**
   - Links to GitHub
   - Copyright/license
   - Contact info (optional)

---

## 🔐 Privacy & Security

- GitHub Pages is free and public
- Your repository is public
- No sensitive data in repository
- Git history is preserved
- Easy to make repository private later

---

## 💡 Next Ideas

After setup, consider:
- 📊 Add statistics dashboard
- 🗣️ Add discussion forum (GitHub Discussions)
- 📧 Add newsletter signup
- 🎥 Add video tutorials
- 🏆 Add user contributions showcase
- 📈 Track analytics with Google Analytics

---

## 📞 Support

For issues:
1. Check COMPREHENSIVE_README.md troubleshooting section
2. Check GitHub Actions logs
3. Create GitHub issue in your repository
4. Check Figma API documentation
5. Ask on GitHub Discussions

---

## 🎉 You're All Set!

Your quantum mechanics animation website is ready to share with the world!

```
https://YOUR_USERNAME.github.io/animation_quantum_mech_basics
```

**Share it on:**
- LinkedIn
- Twitter
- Reddit
- Facebook
- Email
- Resume/Portfolio

---

**Estimated Setup Time**: 30 minutes  
**Estimated Animation Time**: 30 minutes - 2 hours (optional)  
**Figma Integration**: 10 minutes (optional)  

**Total**: 1 hour to fully deployed website!

---

*Generated: October 2025*  
*Quantum Mechanics Animation Pipeline v2.0*
