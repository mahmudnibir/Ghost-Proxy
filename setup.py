from setuptools import setup, find_packages

setup(
    name='YourProjectName',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyautogui',
        'pygetwindow',
        'pyperclip',
        'SpeechRecognition',
        'pyttsx3',
        'pywinauto',
        'pypiwin32',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'your-script=your_module:main_function',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    license='MIT',
)
