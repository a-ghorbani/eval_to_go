from setuptools import setup, find_packages

setup(
    name='eval_to_go',
    version='0.1.1',
    author='Asghar Ghorbani',
    author_email='ghorbani59@gmail.com',
    packages=find_packages(),
    description='Your go-to, no-fuss eval for zapping through RAG and LLM evaluations! For a busy person who\'s too swamped to wrestle with the behemoths of professional setups',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas>=2.0.0',
        'openai>=0.10.0',
        'h2ogpte>=1.3.0',
        'python-dotenv>=1.0.0'
    ],
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
