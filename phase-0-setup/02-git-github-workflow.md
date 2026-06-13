# 02 — Git + GitHub Workflow

Git is how you save your work, track changes, and share your code publicly. Every lesson you complete should be committed.

---

## Step 1: Install Git

```bash
sudo apt install git -y
git --version   # should print git version 2.x
```

## Step 2: Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Step 3: Fork this repo

1. Go to [github.com/only1angelnath/python-for-blockchain-analytics](https://github.com/only1angelnath/python-for-blockchain-analytics)
2. Click **Fork** (top right)
3. This creates a copy at `github.com/YOUR_USERNAME/python-for-blockchain-analytics`

## Step 4: Clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/python-for-blockchain-analytics.git
cd python-for-blockchain-analytics
```

## Step 5: The commit loop

Every time you complete a lesson or exercise:

```bash
git add .
git commit -m "phase-1/week-02: completed syntax exercises"
git push
```

Good commit message format: `phase-N/week-NN: what you did`

## Step 6: Staying up to date

If the original course repo gets updated:

```bash
git remote add upstream https://github.com/only1angelnath/python-for-blockchain-analytics.git
git fetch upstream
git merge upstream/main
```

---

## Your first commit milestone

1. Open `phase-0-setup/README.md`
2. Add your name and start date at the bottom
3. Commit and push

```bash
git add phase-0-setup/README.md
git commit -m "phase-0: started the course — YOUR_NAME"
git push
```

Post your first commit link. You've started. 🚀
