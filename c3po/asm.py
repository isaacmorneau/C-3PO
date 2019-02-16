#source: https://www.felixcloutier.com/x86/AAD
AAD_opts = [
    [0xD5],
]
#source: https://www.felixcloutier.com/x86/AAM
AAM_opts = [
    [0xD4],
]
#source: https://www.felixcloutier.com/x86/ADC
ADC_opts = [
    [0x10],
    [0x11],
    [0x12],
    [0x13],
    [0x14],
    [0x15],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/ADCX
ADCX_opts = [
    [0x66],
    [0x66,0x0F,0x38,0xF6],
]
#source: https://www.felixcloutier.com/x86/ADD
ADD_opts = [
    [0x00],
    [0x01],
    [0x02],
    [0x03],
    [0x04],
    [0x05],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/ADDPD
ADDPD_opts = [
    [0x66,0x0F,0x58],
]
#source: https://www.felixcloutier.com/x86/ADDSD
ADDSD_opts = [
    [0xF2,0x0F,0x58],
]
#source: https://www.felixcloutier.com/x86/ADDSS
ADDSS_opts = [
    [0xF3,0x0F,0x58],
]
#source: https://www.felixcloutier.com/x86/ADDSUBPD
ADDSUBPD_opts = [
    [0x66,0x0F,0xD0],
]
#source: https://www.felixcloutier.com/x86/ADDSUBPS
ADDSUBPS_opts = [
    [0xF2,0x0F,0xD0],
]
#source: https://www.felixcloutier.com/x86/ADOX
ADOX_opts = [
    [0xF3],
    [0xF3,0x0F,0x38,0xF6],
]
#source: https://www.felixcloutier.com/x86/AESDEC
AESDEC_opts = [
    [0x66,0x0F,0x38,0xDE],
]
#source: https://www.felixcloutier.com/x86/AESDECLAST
AESDECLAST_opts = [
    [0x66,0x0F,0x38,0xDF],
]
#source: https://www.felixcloutier.com/x86/AESENC
AESENC_opts = [
    [0x66,0x0F,0x38,0xDC],
]
#source: https://www.felixcloutier.com/x86/AESENCLAST
AESENCLAST_opts = [
    [0x66,0x0F,0x38,0xDD],
]
#source: https://www.felixcloutier.com/x86/AESIMC
AESIMC_opts = [
    [0x66,0x0F,0x38,0xDB],
]
#source: https://www.felixcloutier.com/x86/AESKEYGENASSIST
AESKEYGENASSIST_opts = [
    [0x66,0x0F,0x3A,0xDF],
]
#source: https://www.felixcloutier.com/x86/AND
AND_opts = [
    [0x20],
    [0x21],
    [0x22],
    [0x23],
    [0x24],
    [0x25],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/ANDNPD
ANDNPD_opts = [
    [0x66,0x0F,0x55],
]
#source: https://www.felixcloutier.com/x86/ANDPD
ANDPD_opts = [
    [0x66,0x0F,0x54],
]
#source: https://www.felixcloutier.com/x86/ARPL
ARPL_opts = [
    [0x63],
]
#source: https://www.felixcloutier.com/x86/BLENDPD
BLENDPD_opts = [
    [0x66,0x0F,0x3A,0x0D],
]
#source: https://www.felixcloutier.com/x86/BLENDPS
BLENDPS_opts = [
    [0x66,0x0F,0x3A,0x0C],
]
#source: https://www.felixcloutier.com/x86/BLENDVPD
BLENDVPD_opts = [
    [0x66,0x0F,0x38,0x15],
]
#source: https://www.felixcloutier.com/x86/BLENDVPS
BLENDVPS_opts = [
    [0x66,0x0F,0x38,0x14],
]
#source: https://www.felixcloutier.com/x86/BNDCL
BNDCL_opts = [
    [0xF3,0x0F,0x1A],
]
#source: https://www.felixcloutier.com/x86/BNDCU:BNDCN
BNDCU_BNDCN_opts = [
    [0xF2,0x0F,0x1A],
    [0xF2,0x0F,0x1B],
]
#source: https://www.felixcloutier.com/x86/BNDMK
BNDMK_opts = [
    [0xF3,0x0F,0x1B],
]
#source: https://www.felixcloutier.com/x86/BNDMOV
BNDMOV_opts = [
    [0x66,0x0F,0x1A],
    [0x66,0x0F,0x1B],
]
#source: https://www.felixcloutier.com/x86/BOUND
BOUND_opts = [
    [0x62],
]
#source: https://www.felixcloutier.com/x86/BSF
BSF_opts = [
    [0x0F,0xBC],
]
#source: https://www.felixcloutier.com/x86/BSR
BSR_opts = [
    [0x0F,0xBD],
]
#source: https://www.felixcloutier.com/x86/BSWAP
BSWAP_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/BT
BT_opts = [
    [0x0F,0xA3],
    [0x0F,0xBA],
]
#source: https://www.felixcloutier.com/x86/BTC
BTC_opts = [
    [0x0F,0xBA],
    [0x0F,0xBB],
]
#source: https://www.felixcloutier.com/x86/BTR
BTR_opts = [
    [0x0F,0xB3],
    [0x0F,0xBA],
]
#source: https://www.felixcloutier.com/x86/BTS
BTS_opts = [
    [0x0F,0xAB],
    [0x0F,0xBA],
]
#source: https://www.felixcloutier.com/x86/CALL
CALL_opts = [
    [0x9A],
    [0xE8],
    [0xFF],
]
#source: https://www.felixcloutier.com/x86/CLTS
CLTS_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/CLWB
CLWB_opts = [
    [0x66,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/CMOVcc
CMOVcc_opts = [
    [0x0F,0x40],
    [0x0F,0x41],
    [0x0F,0x42],
    [0x0F,0x43],
    [0x0F,0x44],
    [0x0F,0x45],
    [0x0F,0x46],
    [0x0F,0x47],
    [0x0F,0x48],
    [0x0F,0x49],
    [0x0F,0x4A],
    [0x0F,0x4B],
    [0x0F,0x4C],
    [0x0F,0x4D],
    [0x0F,0x4E],
    [0x0F,0x4F],
]
#source: https://www.felixcloutier.com/x86/CMP
CMP_opts = [
    [0x38],
    [0x39],
    [0x3A],
    [0x3B],
    [0x3C],
    [0x3D],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/CMPPD
CMPPD_opts = [
    [0x66,0x0F,0xC2],
]
#source: https://www.felixcloutier.com/x86/CMPSD
CMPSD_opts = [
    [0xF2,0x0F,0xC2],
]
#source: https://www.felixcloutier.com/x86/CMPSS
CMPSS_opts = [
    [0xF3,0x0F,0xC2],
]
#source: https://www.felixcloutier.com/x86/CMPXCHG
CMPXCHG_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/CMPXCHG8B:CMPXCHG16B
CMPXCHG8B_CMPXCHG16B_opts = [
    [0x0F,0xC7],
]
#source: https://www.felixcloutier.com/x86/COMISD
COMISD_opts = [
    [0x66,0x0F,0x2F],
]
#source: https://www.felixcloutier.com/x86/CPUID
CPUID_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/CRC32
CRC32_opts = [
    [0xF2],
    [0xF2,0x0F,0x38,0xF0],
    [0xF2,0x0F,0x38,0xF1],
]
#source: https://www.felixcloutier.com/x86/CVTDQ2PD
CVTDQ2PD_opts = [
    [0xF3,0x0F,0xE6],
]
#source: https://www.felixcloutier.com/x86/CVTPD2DQ
CVTPD2DQ_opts = [
    [0xF2,0x0F,0xE6],
]
#source: https://www.felixcloutier.com/x86/CVTPD2PI
CVTPD2PI_opts = [
    [0x66,0x0F,0x2D],
]
#source: https://www.felixcloutier.com/x86/CVTPD2PS
CVTPD2PS_opts = [
    [0x66,0x0F,0x5A],
]
#source: https://www.felixcloutier.com/x86/CVTPI2PD
CVTPI2PD_opts = [
    [0x66,0x0F,0x2A],
]
#source: https://www.felixcloutier.com/x86/CVTPS2DQ
CVTPS2DQ_opts = [
    [0x66,0x0F,0x5B],
]
#source: https://www.felixcloutier.com/x86/CVTSD2SI
CVTSD2SI_opts = [
    [0xF2],
    [0xF2,0x0F,0x2D],
]
#source: https://www.felixcloutier.com/x86/CVTSD2SS
CVTSD2SS_opts = [
    [0xF2,0x0F,0x5A],
]
#source: https://www.felixcloutier.com/x86/CVTSI2SD
CVTSI2SD_opts = [
    [0xF2],
    [0xF2,0x0F,0x2A],
]
#source: https://www.felixcloutier.com/x86/CVTSI2SS
CVTSI2SS_opts = [
    [0xF3],
    [0xF3,0x0F,0x2A],
]
#source: https://www.felixcloutier.com/x86/CVTSS2SD
CVTSS2SD_opts = [
    [0xF3,0x0F,0x5A],
]
#source: https://www.felixcloutier.com/x86/CVTSS2SI
CVTSS2SI_opts = [
    [0xF3],
    [0xF3,0x0F,0x2D],
]
#source: https://www.felixcloutier.com/x86/CVTTPD2DQ
CVTTPD2DQ_opts = [
    [0x66,0x0F,0xE6],
]
#source: https://www.felixcloutier.com/x86/CVTTPD2PI
CVTTPD2PI_opts = [
    [0x66,0x0F,0x2C],
]
#source: https://www.felixcloutier.com/x86/CVTTPS2DQ
CVTTPS2DQ_opts = [
    [0xF3,0x0F,0x5B],
]
#source: https://www.felixcloutier.com/x86/CVTTSD2SI
CVTTSD2SI_opts = [
    [0xF2],
    [0xF2,0x0F,0x2C],
]
#source: https://www.felixcloutier.com/x86/CVTTSS2SI
CVTTSS2SI_opts = [
    [0xF3],
    [0xF3,0x0F,0x2C],
]
#source: https://www.felixcloutier.com/x86/DEC
DEC_opts = [
    [0xFE],
    [0xFF],
]
#source: https://www.felixcloutier.com/x86/DIV
DIV_opts = [
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/DIVPD
DIVPD_opts = [
    [0x66,0x0F,0x5E],
]
#source: https://www.felixcloutier.com/x86/DIVSD
DIVSD_opts = [
    [0xF2,0x0F,0x5E],
]
#source: https://www.felixcloutier.com/x86/DIVSS
DIVSS_opts = [
    [0xF3,0x0F,0x5E],
]
#source: https://www.felixcloutier.com/x86/DPPD
DPPD_opts = [
    [0x66,0x0F,0x3A,0x41],
]
#source: https://www.felixcloutier.com/x86/DPPS
DPPS_opts = [
    [0x66,0x0F,0x3A,0x40],
]
#source: https://www.felixcloutier.com/x86/EGETKEY
EGETKEY_opts = [
    [0x16],
    [0x64],
]
#source: https://www.felixcloutier.com/x86/ENTER
ENTER_opts = [
    [0xC8],
]
#source: https://www.felixcloutier.com/x86/EXTRACTPS
EXTRACTPS_opts = [
    [0x66,0x0F,0x3A,0x17],
]
#source: https://www.felixcloutier.com/x86/F2XM1
F2XM1_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FABS
FABS_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FADD:FADDP:FIADD
FADD_FADDP_FIADD_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FBLD
FBLD_opts = [
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FBSTP
FBSTP_opts = [
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FCHS
FCHS_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FCLEX:FNCLEX
FCLEX_FNCLEX_opts = [
    [0x9B,0xDB],
    [0xDB],
]
#source: https://www.felixcloutier.com/x86/FCMOVcc
FCMOVcc_opts = [
    [0xDA],
    [0xDB],
]
#source: https://www.felixcloutier.com/x86/FCOM:FCOMP:FCOMPP
FCOM_FCOMP_FCOMPP_opts = [
    [0xD8],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FCOMI:FCOMIP:FUCOMI:FUCOMIP
FCOMI_FCOMIP_FUCOMI_FUCOMIP_opts = [
    [0xDB],
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FCOS
FCOS_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FDECSTP
FDECSTP_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FDIV:FDIVP:FIDIV
FDIV_FDIVP_FIDIV_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FDIVR:FDIVRP:FIDIVR
FDIVR_FDIVRP_FIDIVR_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FFREE
FFREE_opts = [
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FICOM:FICOMP
FICOM_FICOMP_opts = [
    [0xDA],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FILD
FILD_opts = [
    [0xDB],
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FINCSTP
FINCSTP_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FINIT:FNINIT
FINIT_FNINIT_opts = [
    [0x9B,0xDB],
    [0xDB],
]
#source: https://www.felixcloutier.com/x86/FIST:FISTP
FIST_FISTP_opts = [
    [0xDB],
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FISTTP
FISTTP_opts = [
    [0xDB],
    [0xDD],
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FLD
FLD_opts = [
    [0xD9],
    [0xDB],
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FLD1:FLDL2T:FLDL2E:FLDPI:FLDLG2:FLDLN2:FLDZ
FLD1_FLDL2T_FLDL2E_FLDPI_FLDLG2_FLDLN2_FLDZ_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FLDCW
FLDCW_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FLDENV
FLDENV_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FMUL:FMULP:FIMUL
FMUL_FMULP_FIMUL_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FNOP
FNOP_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FPATAN
FPATAN_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FPREM
FPREM_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FPREM1
FPREM1_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FPTAN
FPTAN_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FRNDINT
FRNDINT_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FRSTOR
FRSTOR_opts = [
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FSAVE:FNSAVE
FSAVE_FNSAVE_opts = [
    [0x9B,0xDD],
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FSCALE
FSCALE_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FSIN
FSIN_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FSINCOS
FSINCOS_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FSQRT
FSQRT_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FSTCW:FNSTCW
FSTCW_FNSTCW_opts = [
    [0x9B,0xD9],
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FSTENV:FNSTENV
FSTENV_FNSTENV_opts = [
    [0x9B,0xD9],
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FST:FSTP
FST_FSTP_opts = [
    [0xD9],
    [0xDB],
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FSTSW:FNSTSW
FSTSW_FNSTSW_opts = [
    [0x9B,0xDD],
    [0x9B,0xDF],
    [0xDD],
    [0xDF],
]
#source: https://www.felixcloutier.com/x86/FSUB:FSUBP:FISUB
FSUB_FSUBP_FISUB_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FSUBR:FSUBRP:FISUBR
FSUBR_FSUBRP_FISUBR_opts = [
    [0xD8],
    [0xDA],
    [0xDC],
    [0xDE],
]
#source: https://www.felixcloutier.com/x86/FTST
FTST_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FUCOM:FUCOMP:FUCOMPP
FUCOM_FUCOMP_FUCOMPP_opts = [
    [0xDA],
    [0xDD],
]
#source: https://www.felixcloutier.com/x86/FXAM
FXAM_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FXCH
FXCH_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FXSAVE
FXSAVE_opts = [
    [0x00],
    [0x11],
    [0x13],
    [0x15],
]
#source: https://www.felixcloutier.com/x86/FXTRACT
FXTRACT_opts = [
    [0xD9,0xF4],
]
#source: https://www.felixcloutier.com/x86/FYL2X
FYL2X_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/FYL2XP1
FYL2XP1_opts = [
    [0xD9],
]
#source: https://www.felixcloutier.com/x86/GF2P8AFFINEINVQB
GF2P8AFFINEINVQB_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/GF2P8AFFINEQB
GF2P8AFFINEQB_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/GF2P8MULB
GF2P8MULB_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/HADDPD
HADDPD_opts = [
    [0x66,0x0F,0x7C],
]
#source: https://www.felixcloutier.com/x86/HADDPS
HADDPS_opts = [
    [0xF2,0x0F,0x7C],
]
#source: https://www.felixcloutier.com/x86/HSUBPD
HSUBPD_opts = [
    [0x66,0x0F,0x7D],
]
#source: https://www.felixcloutier.com/x86/HSUBPS
HSUBPS_opts = [
    [0xF2,0x0F,0x7D],
]
#source: https://www.felixcloutier.com/x86/IDIV
IDIV_opts = [
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/IMUL
IMUL_opts = [
    [0x0F,0xAF],
    [0x69],
    [0x6B],
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/IN
IN_opts = [
    [0xE4],
    [0xE5],
]
#source: https://www.felixcloutier.com/x86/INC
INC_opts = [
    [0xFE],
    [0xFF],
]
#source: https://www.felixcloutier.com/x86/INSERTPS
INSERTPS_opts = [
    [0x66,0x0F,0x3A,0x21],
]
#source: https://www.felixcloutier.com/x86/INTn:INTO:INT3:INT1
INTn_INTO_INT3_INT1_opts = [
    [0xCD],
]
#source: https://www.felixcloutier.com/x86/INVD
INVD_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/INVPCID
INVPCID_opts = [
    [0x66,0x0F,0x38,0x82],
]
#source: https://www.felixcloutier.com/x86/Jcc
Jcc_opts = [
    [0x0F,0x80],
    [0x0F,0x81],
    [0x0F,0x82],
    [0x0F,0x83],
    [0x0F,0x84],
    [0x0F,0x85],
    [0x0F,0x86],
    [0x0F,0x87],
    [0x0F,0x88],
    [0x0F,0x89],
    [0x0F,0x8A],
    [0x0F,0x8B],
    [0x0F,0x8C],
    [0x0F,0x8D],
    [0x0F,0x8E],
    [0x0F,0x8F],
    [0x70],
    [0x71],
    [0x72],
    [0x73],
    [0x74],
    [0x75],
    [0x76],
    [0x77],
    [0x78],
    [0x79],
    [0x7A],
    [0x7B],
    [0x7C],
    [0x7D],
    [0x7E],
    [0x7F],
    [0xE3],
]
#source: https://www.felixcloutier.com/x86/JMP
JMP_opts = [
    [0xE9],
    [0xEA],
    [0xEB],
    [0xFF],
]
#source: https://www.felixcloutier.com/x86/LAR
LAR_opts = [
    [0x0F,0x02],
]
#source: https://www.felixcloutier.com/x86/LDDQU
LDDQU_opts = [
    [0xF2,0x0F,0xF0],
]
#source: https://www.felixcloutier.com/x86/LDS:LES:LFS:LGS:LSS
LDS_LES_LFS_LGS_LSS_opts = [
    [0x0F,0xB2],
    [0x0F,0xB4],
    [0x0F,0xB5],
    [0xC4],
    [0xC5],
]
#source: https://www.felixcloutier.com/x86/LEA
LEA_opts = [
    [0x8D],
]
#source: https://www.felixcloutier.com/x86/LGDT:LIDT
LGDT_LIDT_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/LLDT
LLDT_opts = [
    [0x0F,0x00],
]
#source: https://www.felixcloutier.com/x86/LMSW
LMSW_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/LOOP:LOOPcc
LOOP_LOOPcc_opts = [
    [0xE0],
    [0xE1],
    [0xE2],
]
#source: https://www.felixcloutier.com/x86/LSL
LSL_opts = [
    [0x0F,0x03],
]
#source: https://www.felixcloutier.com/x86/LTR
LTR_opts = [
    [0x0F,0x00],
]
#source: https://www.felixcloutier.com/x86/LZCNT
LZCNT_opts = [
    [0xF3],
    [0xF3,0x0F,0xBD],
]
#source: https://www.felixcloutier.com/x86/MASKMOVDQU
MASKMOVDQU_opts = [
    [0x66,0x0F,0xF7],
]
#source: https://www.felixcloutier.com/x86/MAXPD
MAXPD_opts = [
    [0x66,0x0F,0x5F],
]
#source: https://www.felixcloutier.com/x86/MAXSD
MAXSD_opts = [
    [0xF2,0x0F,0x5F],
]
#source: https://www.felixcloutier.com/x86/MAXSS
MAXSS_opts = [
    [0xF3,0x0F,0x5F],
]
#source: https://www.felixcloutier.com/x86/MINPD
MINPD_opts = [
    [0x66,0x0F,0x5D],
]
#source: https://www.felixcloutier.com/x86/MINSD
MINSD_opts = [
    [0xF2,0x0F,0x5D],
]
#source: https://www.felixcloutier.com/x86/MINSS
MINSS_opts = [
    [0xF3,0x0F,0x5D],
]
#source: https://www.felixcloutier.com/x86/MOV
MOV_opts = [
    [0x88],
    [0x89],
    [0x8A],
    [0x8B],
    [0x8C],
    [0x8E],
    [0xC6],
    [0xC7],
]
#source: https://www.felixcloutier.com/x86/MOV-1
MOV_1_opts = [
    [0x0F],
    [0x0F,0x22],
]
#source: https://www.felixcloutier.com/x86/MOV-2
MOV_2_opts = [
    [0x0F],
    [0x0F,0x23],
]
#source: https://www.felixcloutier.com/x86/MOVAPD
MOVAPD_opts = [
    [0x66,0x0F,0x28],
    [0x66,0x0F,0x29],
]
#source: https://www.felixcloutier.com/x86/MOVDDUP
MOVDDUP_opts = [
    [0xF2,0x0F,0x12],
]
#source: https://www.felixcloutier.com/x86/MOVDIR64B
MOVDIR64B_opts = [
    [0x66,0x0F,0x38,0xF8],
]
#source: https://www.felixcloutier.com/x86/MOVD:MOVQ
MOVD_MOVQ_opts = [
    [0x66],
    [0x66,0x0F,0x6E],
    [0x66,0x0F,0x7E],
]
#source: https://www.felixcloutier.com/x86/MOVDQA:VMOVDQA32:VMOVDQA64
MOVDQA_VMOVDQA32_VMOVDQA64_opts = [
    [0x66,0x0F,0x6F],
    [0x66,0x0F,0x7F],
]
#source: https://www.felixcloutier.com/x86/MOVDQU:VMOVDQU8:VMOVDQU16:VMOVDQU32:VMOVDQU64
MOVDQU_VMOVDQU8_VMOVDQU16_VMOVDQU32_VMOVDQU64_opts = [
    [0xF3,0x0F,0x6F],
    [0xF3,0x0F,0x7F],
]
#source: https://www.felixcloutier.com/x86/MOVHPD
MOVHPD_opts = [
    [0x66,0x0F,0x16],
    [0x66,0x0F,0x17],
]
#source: https://www.felixcloutier.com/x86/MOVLPD
MOVLPD_opts = [
    [0x66,0x0F],
    [0x66,0x0F,0x12],
]
#source: https://www.felixcloutier.com/x86/MOVLPS
MOVLPS_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/MOVMSKPD
MOVMSKPD_opts = [
    [0x66,0x0F,0x50],
]
#source: https://www.felixcloutier.com/x86/MOVNTDQ
MOVNTDQ_opts = [
    [0x66,0x0F,0xE7],
]
#source: https://www.felixcloutier.com/x86/MOVNTDQA
MOVNTDQA_opts = [
    [0x66,0x0F,0x38,0x2A],
]
#source: https://www.felixcloutier.com/x86/MOVNTPD
MOVNTPD_opts = [
    [0x66,0x0F,0x2B],
]
#source: https://www.felixcloutier.com/x86/MOVQ
MOVQ_opts = [
    [0x66,0x0F,0xD6],
    [0xF3,0x0F,0x7E],
]
#source: https://www.felixcloutier.com/x86/MOVQ2DQ
MOVQ2DQ_opts = [
    [0xF3,0x0F,0xD6],
]
#source: https://www.felixcloutier.com/x86/MOVSD
MOVSD_opts = [
    [0xF2,0x0F,0x10],
    [0xF2,0x0F,0x11],
]
#source: https://www.felixcloutier.com/x86/MOVSHDUP
MOVSHDUP_opts = [
    [0xF3,0x0F,0x16],
]
#source: https://www.felixcloutier.com/x86/MOVSLDUP
MOVSLDUP_opts = [
    [0xF3,0x0F,0x12],
]
#source: https://www.felixcloutier.com/x86/MOVSS
MOVSS_opts = [
    [0xF3,0x0F,0x10],
    [0xF3,0x0F,0x11],
]
#source: https://www.felixcloutier.com/x86/MOVSX:MOVSXD
MOVSX_MOVSXD_opts = [
    [0x0F,0xBE],
    [0x0F,0xBF],
    [0x63],
]
#source: https://www.felixcloutier.com/x86/MOVUPD
MOVUPD_opts = [
    [0x66,0x0F,0x10],
    [0x66,0x0F,0x11],
]
#source: https://www.felixcloutier.com/x86/MOVZX
MOVZX_opts = [
    [0x0F,0xB6],
    [0x0F,0xB7],
]
#source: https://www.felixcloutier.com/x86/MPSADBW
MPSADBW_opts = [
    [0x66,0x0F,0x3A,0x42],
]
#source: https://www.felixcloutier.com/x86/MUL
MUL_opts = [
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/MULPD
MULPD_opts = [
    [0x66,0x0F,0x59],
]
#source: https://www.felixcloutier.com/x86/MULSD
MULSD_opts = [
    [0xF2,0x0F,0x59],
]
#source: https://www.felixcloutier.com/x86/MULSS
MULSS_opts = [
    [0xF3,0x0F,0x59],
]
#source: https://www.felixcloutier.com/x86/MWAIT
MWAIT_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/NEG
NEG_opts = [
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/NOP
NOP_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/NOT
NOT_opts = [
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/OR
OR_opts = [
    [0x08],
    [0x09],
    [0x0A],
    [0x0B],
    [0x0C],
    [0x0D],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/ORPD
ORPD_opts = [
    [0x66,0x0F],
]
#source: https://www.felixcloutier.com/x86/OUT
OUT_opts = [
    [0xE6],
    [0xE7],
]
#source: https://www.felixcloutier.com/x86/PABSB:PABSW:PABSD:PABSQ
PABSB_PABSW_PABSD_PABSQ_opts = [
    [0x66,0x0F,0x38,0x1C],
    [0x66,0x0F,0x38,0x1D],
    [0x66,0x0F,0x38,0x1E],
]
#source: https://www.felixcloutier.com/x86/PACKSSWB:PACKSSDW
PACKSSWB_PACKSSDW_opts = [
    [0x66,0x0F,0x63],
    [0x66,0x0F,0x6B],
]
#source: https://www.felixcloutier.com/x86/PACKUSDW
PACKUSDW_opts = [
    [0x66,0x0F,0x38,0x2B],
]
#source: https://www.felixcloutier.com/x86/PACKUSWB
PACKUSWB_opts = [
    [0x66,0x0F,0x67],
]
#source: https://www.felixcloutier.com/x86/PADDB:PADDW:PADDD:PADDQ
PADDB_PADDW_PADDD_PADDQ_opts = [
    [0x66,0x0F,0xD4],
    [0x66,0x0F,0xFC],
    [0x66,0x0F,0xFD],
    [0x66,0x0F,0xFE],
]
#source: https://www.felixcloutier.com/x86/PADDSB:PADDSW
PADDSB_PADDSW_opts = [
    [0x66,0x0F,0xEC],
    [0x66,0x0F,0xED],
]
#source: https://www.felixcloutier.com/x86/PADDUSB:PADDUSW
PADDUSB_PADDUSW_opts = [
    [0x66,0x0F,0xDC],
    [0x66,0x0F,0xDD],
]
#source: https://www.felixcloutier.com/x86/PALIGNR
PALIGNR_opts = [
    [0x66,0x0F,0x3A,0x0F],
]
#source: https://www.felixcloutier.com/x86/PAND
PAND_opts = [
    [0x66,0x0F,0xDB],
]
#source: https://www.felixcloutier.com/x86/PANDN
PANDN_opts = [
    [0x66,0x0F,0xDF],
]
#source: https://www.felixcloutier.com/x86/PAUSE
PAUSE_opts = [
    [0xF3],
]
#source: https://www.felixcloutier.com/x86/PAVGB:PAVGW
PAVGB_PAVGW_opts = [
    [0x66,0x0F],
    [0x66,0x0F,0xE3],
]
#source: https://www.felixcloutier.com/x86/PBLENDVB
PBLENDVB_opts = [
    [0x66,0x0F,0x38,0x10],
]
#source: https://www.felixcloutier.com/x86/PBLENDW
PBLENDW_opts = [
    [0x66,0x0F,0x3A,0x0E],
]
#source: https://www.felixcloutier.com/x86/PCLMULQDQ
PCLMULQDQ_opts = [
    [0x66,0x0F,0x3A,0x44],
]
#source: https://www.felixcloutier.com/x86/PCMPEQB:PCMPEQW:PCMPEQD
PCMPEQB_PCMPEQW_PCMPEQD_opts = [
    [0x66,0x0F,0x74],
    [0x66,0x0F,0x75],
    [0x66,0x0F,0x76],
]
#source: https://www.felixcloutier.com/x86/PCMPEQQ
PCMPEQQ_opts = [
    [0x66,0x0F,0x38,0x29],
]
#source: https://www.felixcloutier.com/x86/PCMPESTRI
PCMPESTRI_opts = [
    [0x16],
    [0x32],
    [0x64],
    [0x66,0x0F,0x3A,0x61],
]
#source: https://www.felixcloutier.com/x86/PCMPESTRM
PCMPESTRM_opts = [
    [0x16],
    [0x32],
    [0x64],
    [0x66,0x0F,0x3A,0x60],
]
#source: https://www.felixcloutier.com/x86/PCMPGTB:PCMPGTW:PCMPGTD
PCMPGTB_PCMPGTW_PCMPGTD_opts = [
    [0x66,0x0F,0x64],
    [0x66,0x0F,0x65],
    [0x66,0x0F,0x66],
]
#source: https://www.felixcloutier.com/x86/PCMPGTQ
PCMPGTQ_opts = [
    [0x66,0x0F,0x38,0x37],
]
#source: https://www.felixcloutier.com/x86/PCMPISTRI
PCMPISTRI_opts = [
    [0x16],
    [0x32],
    [0x64],
    [0x66,0x0F,0x3A,0x63],
]
#source: https://www.felixcloutier.com/x86/PCMPISTRM
PCMPISTRM_opts = [
    [0x16],
    [0x32],
    [0x64],
    [0x66,0x0F,0x3A,0x62],
]
#source: https://www.felixcloutier.com/x86/PEXTRB:PEXTRD:PEXTRQ
PEXTRB_PEXTRD_PEXTRQ_opts = [
    [0x66],
    [0x66,0x0F,0x3A,0x14],
    [0x66,0x0F,0x3A,0x16],
]
#source: https://www.felixcloutier.com/x86/PEXTRW
PEXTRW_opts = [
    [0x66,0x0F,0x3A,0x15],
    [0x66,0x0F,0xC5],
]
#source: https://www.felixcloutier.com/x86/PHADDSW
PHADDSW_opts = [
    [0x66,0x0F,0x38,0x03],
]
#source: https://www.felixcloutier.com/x86/PHADDW:PHADDD
PHADDW_PHADDD_opts = [
    [0x66,0x0F,0x38,0x01],
    [0x66,0x0F,0x38,0x02],
]
#source: https://www.felixcloutier.com/x86/PHMINPOSUW
PHMINPOSUW_opts = [
    [0x66,0x0F,0x38,0x41],
]
#source: https://www.felixcloutier.com/x86/PHSUBSW
PHSUBSW_opts = [
    [0x66,0x0F,0x38,0x07],
]
#source: https://www.felixcloutier.com/x86/PHSUBW:PHSUBD
PHSUBW_PHSUBD_opts = [
    [0x66,0x0F,0x38,0x05],
    [0x66,0x0F,0x38,0x06],
]
#source: https://www.felixcloutier.com/x86/PINSRB:PINSRD:PINSRQ
PINSRB_PINSRD_PINSRQ_opts = [
    [0x66],
    [0x66,0x0F,0x3A,0x20],
    [0x66,0x0F,0x3A,0x22],
]
#source: https://www.felixcloutier.com/x86/PINSRW
PINSRW_opts = [
    [0x66,0x0F,0xC4],
]
#source: https://www.felixcloutier.com/x86/PMADDUBSW
PMADDUBSW_opts = [
    [0x66,0x0F,0x38,0x04],
]
#source: https://www.felixcloutier.com/x86/PMADDWD
PMADDWD_opts = [
    [0x66,0x0F,0xF5],
]
#source: https://www.felixcloutier.com/x86/PMAXSB:PMAXSW:PMAXSD:PMAXSQ
PMAXSB_PMAXSW_PMAXSD_PMAXSQ_opts = [
    [0x66,0x0F,0x38,0x3C],
    [0x66,0x0F,0x38,0x3D],
    [0x66,0x0F,0xEE],
]
#source: https://www.felixcloutier.com/x86/PMAXUB:PMAXUW
PMAXUB_PMAXUW_opts = [
    [0x66,0x0F,0x38],
    [0x66,0x0F,0xDE],
]
#source: https://www.felixcloutier.com/x86/PMAXUD:PMAXUQ
PMAXUD_PMAXUQ_opts = [
    [0x66,0x0F,0x38,0x3F],
]
#source: https://www.felixcloutier.com/x86/PMINSB:PMINSW
PMINSB_PMINSW_opts = [
    [0x66,0x0F,0x38,0x38],
    [0x66,0x0F,0xEA],
]
#source: https://www.felixcloutier.com/x86/PMINSD:PMINSQ
PMINSD_PMINSQ_opts = [
    [0x66,0x0F,0x38,0x39],
]
#source: https://www.felixcloutier.com/x86/PMINUB:PMINUW
PMINUB_PMINUW_opts = [
    [0x66,0x0F,0x38],
    [0x66,0x0F,0xDA],
]
#source: https://www.felixcloutier.com/x86/PMINUD:PMINUQ
PMINUD_PMINUQ_opts = [
    [0x66,0x0F,0x38,0x3B],
]
#source: https://www.felixcloutier.com/x86/PMOVMSKB
PMOVMSKB_opts = [
    [0x66,0x0F,0xD7],
]
#source: https://www.felixcloutier.com/x86/PMOVSX
PMOVSX_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/PMOVZX
PMOVZX_opts = [
    [0x66],
]
#source: https://www.felixcloutier.com/x86/PMULDQ
PMULDQ_opts = [
    [0x66,0x0F,0x38,0x28],
]
#source: https://www.felixcloutier.com/x86/PMULHRSW
PMULHRSW_opts = [
    [0x66,0x0F,0x38,0x0B],
]
#source: https://www.felixcloutier.com/x86/PMULHUW
PMULHUW_opts = [
    [0x66,0x0F,0xE4],
]
#source: https://www.felixcloutier.com/x86/PMULHW
PMULHW_opts = [
    [0x66,0x0F,0xE5],
]
#source: https://www.felixcloutier.com/x86/PMULLD:PMULLQ
PMULLD_PMULLQ_opts = [
    [0x66,0x0F,0x38,0x40],
]
#source: https://www.felixcloutier.com/x86/PMULLW
PMULLW_opts = [
    [0x66,0x0F,0xD5],
]
#source: https://www.felixcloutier.com/x86/PMULUDQ
PMULUDQ_opts = [
    [0x66,0x0F,0xF4],
]
#source: https://www.felixcloutier.com/x86/POP
POP_opts = [
    [0x0F],
    [0x8F],
]
#source: https://www.felixcloutier.com/x86/POPCNT
POPCNT_opts = [
    [0xF3],
    [0xF3,0x0F,0xB8],
]
#source: https://www.felixcloutier.com/x86/POR
POR_opts = [
    [0x66,0x0F,0xEB],
]
#source: https://www.felixcloutier.com/x86/PREFETCHh
PREFETCHh_opts = [
    [0x0F,0x18],
]
#source: https://www.felixcloutier.com/x86/PREFETCHW
PREFETCHW_opts = [
    [0x0F,0x0D],
]
#source: https://www.felixcloutier.com/x86/PREFETCHWT1
PREFETCHWT1_opts = [
    [0x0F,0x0D],
]
#source: https://www.felixcloutier.com/x86/PSADBW
PSADBW_opts = [
    [0x66,0x0F,0xF6],
]
#source: https://www.felixcloutier.com/x86/PSHUFB
PSHUFB_opts = [
    [0x66,0x0F,0x38,0x00],
]
#source: https://www.felixcloutier.com/x86/PSHUFD
PSHUFD_opts = [
    [0x66,0x0F,0x70],
]
#source: https://www.felixcloutier.com/x86/PSHUFHW
PSHUFHW_opts = [
    [0xF3,0x0F,0x70],
]
#source: https://www.felixcloutier.com/x86/PSHUFLW
PSHUFLW_opts = [
    [0xF2,0x0F,0x70],
]
#source: https://www.felixcloutier.com/x86/PSIGNB:PSIGNW:PSIGND
PSIGNB_PSIGNW_PSIGND_opts = [
    [0x66,0x0F,0x38,0x08],
    [0x66,0x0F,0x38,0x09],
    [0x66,0x0F,0x38,0x0A],
]
#source: https://www.felixcloutier.com/x86/PSLLDQ
PSLLDQ_opts = [
    [0x66,0x0F,0x73],
]
#source: https://www.felixcloutier.com/x86/PSLLW:PSLLD:PSLLQ
PSLLW_PSLLD_PSLLQ_opts = [
    [0x66,0x0F,0x71],
    [0x66,0x0F,0x72],
    [0x66,0x0F,0x73],
    [0x66,0x0F,0xF1],
    [0x66,0x0F,0xF2],
    [0x66,0x0F,0xF3],
]
#source: https://www.felixcloutier.com/x86/PSRAW:PSRAD:PSRAQ
PSRAW_PSRAD_PSRAQ_opts = [
    [0x66,0x0F,0x71],
    [0x66,0x0F,0x72],
    [0x66,0x0F,0xE1],
    [0x66,0x0F,0xE2],
]
#source: https://www.felixcloutier.com/x86/PSRLDQ
PSRLDQ_opts = [
    [0x66,0x0F,0x73],
]
#source: https://www.felixcloutier.com/x86/PSRLW:PSRLD:PSRLQ
PSRLW_PSRLD_PSRLQ_opts = [
    [0x66,0x0F,0x71],
    [0x66,0x0F,0x72],
    [0x66,0x0F,0x73],
    [0x66,0x0F,0xD1],
    [0x66,0x0F,0xD2],
    [0x66,0x0F,0xD3],
]
#source: https://www.felixcloutier.com/x86/PSUBB:PSUBW:PSUBD
PSUBB_PSUBW_PSUBD_opts = [
    [0x66,0x0F,0xF8],
    [0x66,0x0F,0xF9],
    [0x66,0x0F,0xFA],
]
#source: https://www.felixcloutier.com/x86/PSUBQ
PSUBQ_opts = [
    [0x66,0x0F,0xFB],
]
#source: https://www.felixcloutier.com/x86/PSUBSB:PSUBSW
PSUBSB_PSUBSW_opts = [
    [0x66,0x0F,0xE8],
    [0x66,0x0F,0xE9],
]
#source: https://www.felixcloutier.com/x86/PSUBUSB:PSUBUSW
PSUBUSB_PSUBUSW_opts = [
    [0x66,0x0F,0xD8],
    [0x66,0x0F,0xD9],
]
#source: https://www.felixcloutier.com/x86/PTEST
PTEST_opts = [
    [0x66,0x0F,0x38,0x17],
]
#source: https://www.felixcloutier.com/x86/PTWRITE
PTWRITE_opts = [
    [0xF3],
    [0xF3,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/PUNPCKHBW:PUNPCKHWD:PUNPCKHDQ:PUNPCKHQDQ
PUNPCKHBW_PUNPCKHWD_PUNPCKHDQ_PUNPCKHQDQ_opts = [
    [0x66,0x0F,0x68],
    [0x66,0x0F,0x69],
    [0x66,0x0F,0x6A],
    [0x66,0x0F,0x6D],
]
#source: https://www.felixcloutier.com/x86/PUNPCKLBW:PUNPCKLWD:PUNPCKLDQ:PUNPCKLQDQ
PUNPCKLBW_PUNPCKLWD_PUNPCKLDQ_PUNPCKLQDQ_opts = [
    [0x66,0x0F,0x60],
    [0x66,0x0F,0x61],
    [0x66,0x0F,0x62],
    [0x66,0x0F,0x6C],
]
#source: https://www.felixcloutier.com/x86/PUSH
PUSH_opts = [
    [0x0F],
    [0x68],
    [0x6A],
    [0xFF],
]
#source: https://www.felixcloutier.com/x86/PXOR
PXOR_opts = [
    [0x66,0x0F,0xEF],
]
#source: https://www.felixcloutier.com/x86/RCL:RCR:ROL:ROR
RCL_RCR_ROL_ROR_opts = [
    [0xC0],
    [0xC1],
    [0xD0],
    [0xD1],
    [0xD2],
    [0xD3],
]
#source: https://www.felixcloutier.com/x86/RCPSS
RCPSS_opts = [
    [0xF3,0x0F,0x53],
]
#source: https://www.felixcloutier.com/x86/RDFSBASE:RDGSBASE
RDFSBASE_RDGSBASE_opts = [
    [0xF3],
]
#source: https://www.felixcloutier.com/x86/RDPID
RDPID_opts = [
    [0xF3,0x0F,0xC7],
]
#source: https://www.felixcloutier.com/x86/RDPMC
RDPMC_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/RDTSC
RDTSC_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/RDTSCP
RDTSCP_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/REP:REPE:REPZ:REPNE:REPNZ
REP_REPE_REPZ_REPNE_REPNZ_opts = [
    [0xF2],
    [0xF3],
]
#source: https://www.felixcloutier.com/x86/RET
RET_opts = [
    [0xC2],
    [0xCA],
]
#source: https://www.felixcloutier.com/x86/ROUNDPD
ROUNDPD_opts = [
    [0x66,0x0F,0x3A,0x09],
]
#source: https://www.felixcloutier.com/x86/ROUNDPS
ROUNDPS_opts = [
    [0x66,0x0F,0x3A,0x08],
]
#source: https://www.felixcloutier.com/x86/ROUNDSD
ROUNDSD_opts = [
    [0x66,0x0F,0x3A,0x0B],
]
#source: https://www.felixcloutier.com/x86/ROUNDSS
ROUNDSS_opts = [
    [0x66,0x0F,0x3A,0x0A],
]
#source: https://www.felixcloutier.com/x86/RSM
RSM_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/RSQRTSS
RSQRTSS_opts = [
    [0xF3,0x0F,0x52],
]
#source: https://www.felixcloutier.com/x86/SAL:SAR:SHL:SHR
SAL_SAR_SHL_SHR_opts = [
    [0xC0],
    [0xC1],
    [0xD0],
    [0xD1],
    [0xD2],
    [0xD3],
]
#source: https://www.felixcloutier.com/x86/SBB
SBB_opts = [
    [0x18],
    [0x19],
    [0x1A],
    [0x1B],
    [0x1C],
    [0x1D],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/SETcc
SETcc_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/SHLD
SHLD_opts = [
    [0x0F,0xA4],
    [0x0F,0xA5],
]
#source: https://www.felixcloutier.com/x86/SHRD
SHRD_opts = [
    [0x0F,0xAC],
    [0x0F,0xAD],
]
#source: https://www.felixcloutier.com/x86/SHUFPD
SHUFPD_opts = [
    [0x66,0x0F,0xC6],
]
#source: https://www.felixcloutier.com/x86/SIDT
SIDT_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/SLDT
SLDT_opts = [
    [0x0F,0x00],
]
#source: https://www.felixcloutier.com/x86/SMSW
SMSW_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/SQRTPD
SQRTPD_opts = [
    [0x66,0x0F,0x51],
]
#source: https://www.felixcloutier.com/x86/SQRTSD
SQRTSD_opts = [
    [0xF2,0x0F],
]
#source: https://www.felixcloutier.com/x86/SQRTSS
SQRTSS_opts = [
    [0xF3,0x0F,0x51],
]
#source: https://www.felixcloutier.com/x86/STR
STR_opts = [
    [0x0F,0x00],
]
#source: https://www.felixcloutier.com/x86/SUB
SUB_opts = [
    [0x28],
    [0x29],
    [0x2A],
    [0x2B],
    [0x2C],
    [0x2D],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/SUBPD
SUBPD_opts = [
    [0x66,0x0F,0x5C],
]
#source: https://www.felixcloutier.com/x86/SUBSD
SUBSD_opts = [
    [0xF2,0x0F,0x5C],
]
#source: https://www.felixcloutier.com/x86/SUBSS
SUBSS_opts = [
    [0xF3,0x0F,0x5C],
]
#source: https://www.felixcloutier.com/x86/SWAPGS
SWAPGS_opts = [
    [0x0F,0x01],
]
#source: https://www.felixcloutier.com/x86/SYSCALL
SYSCALL_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/SYSENTER
SYSENTER_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/SYSEXIT
SYSEXIT_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/SYSRET
SYSRET_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/TEST
TEST_opts = [
    [0x84],
    [0x85],
    [0xA8],
    [0xA9],
    [0xF6],
    [0xF7],
]
#source: https://www.felixcloutier.com/x86/TPAUSE
TPAUSE_opts = [
    [0x66,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/TZCNT
TZCNT_opts = [
    [0xF3],
    [0xF3,0x0F,0xBC],
]
#source: https://www.felixcloutier.com/x86/UCOMISD
UCOMISD_opts = [
    [0x66,0x0F,0x2E],
]
#source: https://www.felixcloutier.com/x86/UD
UD_opts = [
    [0x0F],
    [0x0F,0xB9],
    [0x0F,0xFF],
]
#source: https://www.felixcloutier.com/x86/UMONITOR
UMONITOR_opts = [
    [0xF3,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/UMWAIT
UMWAIT_opts = [
    [0xF2,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/UNPCKHPD
UNPCKHPD_opts = [
    [0x66,0x0F,0x15],
]
#source: https://www.felixcloutier.com/x86/UNPCKLPD
UNPCKLPD_opts = [
    [0x66,0x0F,0x14],
]
#source: https://www.felixcloutier.com/x86/VERR:VERW
VERR_VERW_opts = [
    [0x0F,0x00],
]
#source: https://www.felixcloutier.com/x86/WBINVD
WBINVD_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/WRFSBASE:WRGSBASE
WRFSBASE_WRGSBASE_opts = [
    [0xF3,0x0F,0xAE],
]
#source: https://www.felixcloutier.com/x86/WRMSR
WRMSR_opts = [
    [0x0F],
]
#source: https://www.felixcloutier.com/x86/XABORT
XABORT_opts = [
    [0xC6,0xF8],
]
#source: https://www.felixcloutier.com/x86/XACQUIRE:XRELEASE
XACQUIRE_XRELEASE_opts = [
    [0xF2],
    [0xF3],
]
#source: https://www.felixcloutier.com/x86/XADD
XADD_opts = [
    [0x0F,0xC0],
    [0x0F,0xC1],
]
#source: https://www.felixcloutier.com/x86/XBEGIN
XBEGIN_opts = [
    [0xC7,0xF8],
]
#source: https://www.felixcloutier.com/x86/XCHG
XCHG_opts = [
    [0x86],
    [0x87],
]
#source: https://www.felixcloutier.com/x86/XOR
XOR_opts = [
    [0x30],
    [0x31],
    [0x32],
    [0x33],
    [0x34],
    [0x35],
    [0x80],
    [0x81],
    [0x83],
]
#source: https://www.felixcloutier.com/x86/XORPD
XORPD_opts = [
    [0x66,0x0F],
]
everyopt = [AAD_opts, AAM_opts, ADC_opts, ADCX_opts, ADD_opts, ADDPD_opts, ADDSD_opts, ADDSS_opts, ADDSUBPD_opts, ADDSUBPS_opts, ADOX_opts, AESDEC_opts, AESDECLAST_opts, AESENC_opts, AESENCLAST_opts, AESIMC_opts, AESKEYGENASSIST_opts, AND_opts, ANDNPD_opts, ANDPD_opts, ARPL_opts, BLENDPD_opts, BLENDPS_opts, BLENDVPD_opts, BLENDVPS_opts, BNDCL_opts, BNDCU_BNDCN_opts, BNDMK_opts, BNDMOV_opts, BOUND_opts, BSF_opts, BSR_opts, BSWAP_opts, BT_opts, BTC_opts, BTR_opts, BTS_opts, CALL_opts, CLTS_opts, CLWB_opts, CMOVcc_opts, CMP_opts, CMPPD_opts, CMPSD_opts, CMPSS_opts, CMPXCHG_opts, CMPXCHG8B_CMPXCHG16B_opts, COMISD_opts, CPUID_opts, CRC32_opts, CVTDQ2PD_opts, CVTPD2DQ_opts, CVTPD2PI_opts, CVTPD2PS_opts, CVTPI2PD_opts, CVTPS2DQ_opts, CVTSD2SI_opts, CVTSD2SS_opts, CVTSI2SD_opts, CVTSI2SS_opts, CVTSS2SD_opts, CVTSS2SI_opts, CVTTPD2DQ_opts, CVTTPD2PI_opts, CVTTPS2DQ_opts, CVTTSD2SI_opts, CVTTSS2SI_opts, DEC_opts, DIV_opts, DIVPD_opts, DIVSD_opts, DIVSS_opts, DPPD_opts, DPPS_opts, EGETKEY_opts, ENTER_opts, EXTRACTPS_opts, F2XM1_opts, FABS_opts, FADD_FADDP_FIADD_opts, FBLD_opts, FBSTP_opts, FCHS_opts, FCLEX_FNCLEX_opts, FCMOVcc_opts, FCOM_FCOMP_FCOMPP_opts, FCOMI_FCOMIP_FUCOMI_FUCOMIP_opts, FCOS_opts, FDECSTP_opts, FDIV_FDIVP_FIDIV_opts, FDIVR_FDIVRP_FIDIVR_opts, FFREE_opts, FICOM_FICOMP_opts, FILD_opts, FINCSTP_opts, FINIT_FNINIT_opts, FIST_FISTP_opts, FISTTP_opts, FLD_opts, FLD1_FLDL2T_FLDL2E_FLDPI_FLDLG2_FLDLN2_FLDZ_opts, FLDCW_opts, FLDENV_opts, FMUL_FMULP_FIMUL_opts, FNOP_opts, FPATAN_opts, FPREM_opts, FPREM1_opts, FPTAN_opts, FRNDINT_opts, FRSTOR_opts, FSAVE_FNSAVE_opts, FSCALE_opts, FSIN_opts, FSINCOS_opts, FSQRT_opts, FSTCW_FNSTCW_opts, FSTENV_FNSTENV_opts, FST_FSTP_opts, FSTSW_FNSTSW_opts, FSUB_FSUBP_FISUB_opts, FSUBR_FSUBRP_FISUBR_opts, FTST_opts, FUCOM_FUCOMP_FUCOMPP_opts, FXAM_opts, FXCH_opts, FXSAVE_opts, FXTRACT_opts, FYL2X_opts, FYL2XP1_opts, GF2P8AFFINEINVQB_opts, GF2P8AFFINEQB_opts, GF2P8MULB_opts, HADDPD_opts, HADDPS_opts, HSUBPD_opts, HSUBPS_opts, IDIV_opts, IMUL_opts, IN_opts, INC_opts, INSERTPS_opts, INTn_INTO_INT3_INT1_opts, INVD_opts, INVPCID_opts, Jcc_opts, JMP_opts, LAR_opts, LDDQU_opts, LDS_LES_LFS_LGS_LSS_opts, LEA_opts, LGDT_LIDT_opts, LLDT_opts, LMSW_opts, LOOP_LOOPcc_opts, LSL_opts, LTR_opts, LZCNT_opts, MASKMOVDQU_opts, MAXPD_opts, MAXSD_opts, MAXSS_opts, MINPD_opts, MINSD_opts, MINSS_opts, MOV_opts, MOV_1_opts, MOV_2_opts, MOVAPD_opts, MOVDDUP_opts, MOVDIR64B_opts, MOVD_MOVQ_opts, MOVDQA_VMOVDQA32_VMOVDQA64_opts, MOVDQU_VMOVDQU8_VMOVDQU16_VMOVDQU32_VMOVDQU64_opts, MOVHPD_opts, MOVLPD_opts, MOVLPS_opts, MOVMSKPD_opts, MOVNTDQ_opts, MOVNTDQA_opts, MOVNTPD_opts, MOVQ_opts, MOVQ2DQ_opts, MOVSD_opts, MOVSHDUP_opts, MOVSLDUP_opts, MOVSS_opts, MOVSX_MOVSXD_opts, MOVUPD_opts, MOVZX_opts, MPSADBW_opts, MUL_opts, MULPD_opts, MULSD_opts, MULSS_opts, MWAIT_opts, NEG_opts, NOP_opts, NOT_opts, OR_opts, ORPD_opts, OUT_opts, PABSB_PABSW_PABSD_PABSQ_opts, PACKSSWB_PACKSSDW_opts, PACKUSDW_opts, PACKUSWB_opts, PADDB_PADDW_PADDD_PADDQ_opts, PADDSB_PADDSW_opts, PADDUSB_PADDUSW_opts, PALIGNR_opts, PAND_opts, PANDN_opts, PAUSE_opts, PAVGB_PAVGW_opts, PBLENDVB_opts, PBLENDW_opts, PCLMULQDQ_opts, PCMPEQB_PCMPEQW_PCMPEQD_opts, PCMPEQQ_opts, PCMPESTRI_opts, PCMPESTRM_opts, PCMPGTB_PCMPGTW_PCMPGTD_opts, PCMPGTQ_opts, PCMPISTRI_opts, PCMPISTRM_opts, PEXTRB_PEXTRD_PEXTRQ_opts, PEXTRW_opts, PHADDSW_opts, PHADDW_PHADDD_opts, PHMINPOSUW_opts, PHSUBSW_opts, PHSUBW_PHSUBD_opts, PINSRB_PINSRD_PINSRQ_opts, PINSRW_opts, PMADDUBSW_opts, PMADDWD_opts, PMAXSB_PMAXSW_PMAXSD_PMAXSQ_opts, PMAXUB_PMAXUW_opts, PMAXUD_PMAXUQ_opts, PMINSB_PMINSW_opts, PMINSD_PMINSQ_opts, PMINUB_PMINUW_opts, PMINUD_PMINUQ_opts, PMOVMSKB_opts, PMOVSX_opts, PMOVZX_opts, PMULDQ_opts, PMULHRSW_opts, PMULHUW_opts, PMULHW_opts, PMULLD_PMULLQ_opts, PMULLW_opts, PMULUDQ_opts, POP_opts, POPCNT_opts, POR_opts, PREFETCHh_opts, PREFETCHW_opts, PREFETCHWT1_opts, PSADBW_opts, PSHUFB_opts, PSHUFD_opts, PSHUFHW_opts, PSHUFLW_opts, PSIGNB_PSIGNW_PSIGND_opts, PSLLDQ_opts, PSLLW_PSLLD_PSLLQ_opts, PSRAW_PSRAD_PSRAQ_opts, PSRLDQ_opts, PSRLW_PSRLD_PSRLQ_opts, PSUBB_PSUBW_PSUBD_opts, PSUBQ_opts, PSUBSB_PSUBSW_opts, PSUBUSB_PSUBUSW_opts, PTEST_opts, PTWRITE_opts, PUNPCKHBW_PUNPCKHWD_PUNPCKHDQ_PUNPCKHQDQ_opts, PUNPCKLBW_PUNPCKLWD_PUNPCKLDQ_PUNPCKLQDQ_opts, PUSH_opts, PXOR_opts, RCL_RCR_ROL_ROR_opts, RCPSS_opts, RDFSBASE_RDGSBASE_opts, RDPID_opts, RDPMC_opts, RDTSC_opts, RDTSCP_opts, REP_REPE_REPZ_REPNE_REPNZ_opts, RET_opts, ROUNDPD_opts, ROUNDPS_opts, ROUNDSD_opts, ROUNDSS_opts, RSM_opts, RSQRTSS_opts, SAL_SAR_SHL_SHR_opts, SBB_opts, SETcc_opts, SHLD_opts, SHRD_opts, SHUFPD_opts, SIDT_opts, SLDT_opts, SMSW_opts, SQRTPD_opts, SQRTSD_opts, SQRTSS_opts, STR_opts, SUB_opts, SUBPD_opts, SUBSD_opts, SUBSS_opts, SWAPGS_opts, SYSCALL_opts, SYSENTER_opts, SYSEXIT_opts, SYSRET_opts, TEST_opts, TPAUSE_opts, TZCNT_opts, UCOMISD_opts, UD_opts, UMONITOR_opts, UMWAIT_opts, UNPCKHPD_opts, UNPCKLPD_opts, VERR_VERW_opts, WBINVD_opts, WRFSBASE_WRGSBASE_opts, WRMSR_opts, XABORT_opts, XACQUIRE_XRELEASE_opts, XADD_opts, XBEGIN_opts, XCHG_opts, XOR_opts, XORPD_opts]
