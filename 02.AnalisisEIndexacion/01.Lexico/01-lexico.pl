#!/user/bin/perl
use utf8;
use open ':encoding(utf8)';
binmode (STDOUT, ":utf8");
system("clear");

#Programa que toma como entrada las etiquetas originales, elimina las etiquetas que incluyen caracteres especiales y numeros , etiquetas con longitud superior a 20 y menor a 2. Devuelve un archivo de error con los errores de las etiquetas y archivo de etiquetas limpias.

use constant logitud_maxima =>  20;
use constant longitud_minima =>  2;

print  ("Creando archivos de salida...\n");
#  Función que retorna un arreglo cargado de Palabras Vacías **
sub pv {
	$args = shift;
	open(IN,"<$args");
	binmode(IN,":utf8");
	while ($linea = <IN>){
		chomp($linea);
		$linea =~ tr/áéíóú/aeiou/;
		$linea =~ tr/[A-Z]/a-z/;
		$vacias[$i++] = $linea;
	}
	close(IN);
	return (@vacias);
}


@palabras_vacias = pv("stopwords.txt");



open (OUT, ">etiquetas.txt"); #Archivo de Salida de etiquetas Limpias
binmode (OUT,":utf8");
open (OUT2, ">error.txt"); #Archivo de errores de etiquetas
binmode (OUT2,":utf8");
open(IN, "etiquetas_or.txt") or die "No se puede abrir el archivo";  
binmode (IN,":utf8");   
$procesados++;
$l=0;
while($line=<IN>)
{
    $l++;
    print "$l\n";
    chomp($line); 
    @array = split(';', $line);
    $etiqueta_or = $array[1];
    $imagen = $array[0];
    $etiqueta = $etiqueta_or;
    $etiqueta =~ tr/áéíóúÁÉÍÓÚäëïöüÄËÏÖÜâêîôûÂÊÎÔÛ/aeiouAEIOUaeiouAEIOUaeiouAEIOU/; # Sacar los acentos y otros
    $etiqueta =~ tr/ñÑ/nN/; # Reemplazar las ñ y Ñ por n y N
    $etiqueta =~ tr/[A-Z]/[a-z]/;# Pasaje de Mayśucualas a Minúsculas
    $etiqueta =~ s/\_//g;  # Sacar las guiones bajos
    $etiqueta =~ s/[\$.,''¿?¡!%#“”‘ï®¨~´=«ç’^—–º¬»\"\[\]\{\}><+¡•…`›¾©;:&·'\(\)|*-]//g;  # Sacar signos de puntuación y otros caracteres especiales
    $etiqueta =~ s/\///g; # Sacar las Barras Laterales
    foreach $k (@palabras_vacias) {$etiqueta =~ s/ $k //g; } # Sacar las palabras vacia    
    if ($etiqueta =~ /[0-9]/){ #Sacar los Numeros
         $etiqueta = ''; 
         }   
    if ( (length($etiqueta) > longitud_minima) and (length($etiqueta) < logitud_maxima)){
           print OUT ("$imagen;$etiqueta\n");			 }           	
    else
       {
       print OUT2 ("$imagen;$etiqueta_or\n");
       }	 
		
             
   }

close (IN);
 close (OUT); 



