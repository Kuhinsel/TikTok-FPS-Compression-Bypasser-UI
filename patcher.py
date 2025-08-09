#!/usr/bin/env python3
import sys

def patch_atom(atom_name, data, scale_factor=None):
    """
    Modifica os átomos 'mvhd' ou 'mdhd' dentro do arquivo MP4 para alterar
    o timescale e a duração, permitindo manipular a velocidade/fps do vídeo.

    Parâmetros:
    - atom_name: string, nome do átomo a ser modificado ('mvhd' ou 'mdhd').
    - data: bytearray, conteúdo binário do arquivo MP4.
    - scale_factor: float ou None, fator de escala para ajustar timescale e duração.
      Se None, calcula automaticamente com base no timescale original.

    Retorna:
    - count: int, número de átomos modificados.
    """

    count = 0
    start = 0
    atom_bytes = atom_name.encode('utf-8')  # converte o nome do átomo para bytes

    while True:
        # procura pelo átomo no arquivo, começando do índice 'start'
        found = data.find(atom_bytes, start)
        if found == -1:
            # não encontrou mais ocorrências do átomo
            break

        header_offset = found - 4  # posição do tamanho do box antes do nome do átomo
        if header_offset < 0:
            # posição inválida, pula pra próxima busca
            start = found + 4
            continue

        # lê o tamanho do box (área do átomo) em bytes (4 bytes big endian)
        box_size = int.from_bytes(data[header_offset:header_offset+4], 'big')
        if box_size < 8:
            # box inválido (tamanho muito pequeno), pula
            start = found + 4
            continue

        version = data[header_offset + 8]  # lê a versão do átomo (byte 8 após header)
        
        if version == 0:
            # Para versão 0, timescale e duration são 4 bytes cada, em offsets fixos
            timescale_offset = header_offset + 20
            duration_offset = header_offset + 24

            # verifica se há espaço suficiente para modificar duration
            if duration_offset + 4 > header_offset + box_size:
                start = found + 4
                continue

            # lê valores antigos (4 bytes cada)
            old_timescale = int.from_bytes(data[timescale_offset:timescale_offset+4], 'big')
            old_duration = int.from_bytes(data[duration_offset:duration_offset+4], 'big')

            # calcula o fator de escala: usa o fornecido ou padrão (30000 / old_timescale)
            chosen_scale = scale_factor or (30000 / old_timescale)
            new_timescale = int(old_timescale * chosen_scale)
            new_duration = int(old_duration * chosen_scale)

            # substitui os bytes originais pelos novos valores
            data[timescale_offset:timescale_offset+4] = new_timescale.to_bytes(4, 'big')
            data[duration_offset:duration_offset+4] = new_duration.to_bytes(4, 'big')

            print(f"Patched {atom_name} at offset {header_offset}: timescale {old_timescale}->{new_timescale}, duration {old_duration}->{new_duration}")
            count += 1

        elif version == 1:
            # Para versão 1, timescale é 4 bytes, duration é 8 bytes, em offsets diferentes
            timescale_offset = header_offset + 28
            duration_offset = header_offset + 32

            # verifica espaço para duration de 8 bytes
            if duration_offset + 8 > header_offset + box_size:
                start = found + 4
                continue

            old_timescale = int.from_bytes(data[timescale_offset:timescale_offset+4], 'big')
            old_duration = int.from_bytes(data[duration_offset:duration_offset+8], 'big')

            chosen_scale = scale_factor or (30000 / old_timescale)
            new_timescale = int(old_timescale * chosen_scale)
            new_duration = int(old_duration * chosen_scale)

            data[timescale_offset:timescale_offset+4] = new_timescale.to_bytes(4, 'big')
            data[duration_offset:duration_offset+8] = new_duration.to_bytes(8, 'big')

            print(f"Patched {atom_name} at offset {header_offset}: timescale {old_timescale}->{new_timescale}, duration {old_duration}->{new_duration}")
            count += 1
        else:
            # versão desconhecida, não modifica
            print(f"Found {atom_name} at offset {header_offset} with unknown version {version}; skipping.")

        start = found + 4  # continua procurando após o último átomo encontrado

    return count

def patch_mp4(input_filename, output_filename, scale_factor=None):
    """
    Abre um arquivo MP4, modifica os átomos 'mvhd' e 'mdhd' para ajustar fps/timescale,
    e salva o arquivo modificado.

    Parâmetros:
    - input_filename: string, caminho do arquivo MP4 original.
    - output_filename: string, caminho para salvar o arquivo modificado.
    - scale_factor: float ou None, fator de escala para ajuste (opcional).
    """

    with open(input_filename, 'rb') as f:
        data = bytearray(f.read())  # lê o arquivo inteiro em memória como bytearray mutável

    # modifica os átomos 'mvhd' e 'mdhd'
    patched_mvhd = patch_atom("mvhd", data, scale_factor)
    patched_mdhd = patch_atom("mdhd", data, scale_factor)

    total_patched = patched_mvhd + patched_mdhd
    print(f"\nTotal patched atoms: {total_patched}")

    # escreve o arquivo modificado
    with open(output_filename, 'wb') as f:
        f.write(data)

    print(f"Patched file written to: {output_filename}")

if __name__ == "__main__":
    # Verifica argumentos de linha de comando
    if len(sys.argv) < 3:
        print("Usage: patch_mp4.py input.mp4 output.mp4 [scale_factor (optional)]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    factor = None

    # tenta converter o scale_factor se fornecido
    if len(sys.argv) > 3:
        try:
            factor = float(sys.argv[3])
        except ValueError:
            print("Invalid scale factor provided. Using automatic adjustment.")

    patch_mp4(input_file, output_file, scale_factor=factor)
