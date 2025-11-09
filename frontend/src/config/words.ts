/**
 * Turkish Words Configuration
 *
 * List of Turkish orthodontic/medical terminology words used for pronunciation testing.
 * Edit this file to add, remove, or modify the word list.
 *
 * Words are presented to participants in the order listed below.
 */

export const turkishWords: string[] = [
  'estetik',
  'teşhis',
  'maloklüzyon',
  'braket',
  'çapraşıklık',
  'temporomandibular',
  'gömük diş',
  'asimetri',
  'aparey',
  'şeffaf braket',
  'florür',
  'sefalometri',
  'ortognatik',
  'kapanış',
  'fonksiyonel',
  'diastema',
  'distalizasyon',
  'profil',
  'frenoktomi',
  'oklüzyon',
  'mandibula',
  'maksilla',
  'overjet',
  'pekiştirme',
  'iskeletsel',
  'ortodonti',
  'röntgen',
  'genişletme',
  'çene travması',
  'kondil',
  'dişlenme',
  'ankiloz',
  'mini vida',
  'diş teli',
  'zigoma',
  'splint',
  'retainer',
  'şeffaf plak',
  'konjenital eksiklik',
  'süpernümere',
];

/**
 * Get total number of words in the test
 */
export const getTotalWords = (): number => turkishWords.length;

/**
 * Get a specific word by index
 */
export const getWord = (index: number): string | undefined => {
  return turkishWords[index];
};

/**
 * Validate if an index is within bounds
 */
export const isValidIndex = (index: number): boolean => {
  return index >= 0 && index < turkishWords.length;
};
