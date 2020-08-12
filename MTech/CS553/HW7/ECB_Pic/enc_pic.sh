identify IITBhilaiLogo.png
convert -depth 32 IITBhilaiLogo.png IITBhilaiLogo.rgba
openssl aes-256-ecb -nosalt -in IITBhilaiLogo.rgba -out 
IITBhilaiLogoEnc.rgba
pass: 'CS553'
convert -size 400x400 -depth 32 IITBhilaiLogoEnc.rgba 
IITBhilaiLogoEnc.png