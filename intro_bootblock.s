	
	dc.b    "DOS",0
    dc.l    0              	; Checksum (Externally Calculated)
    bra.s   boot_entry
    dc.w    0

boot_entry:
	; Move to base address of the custom chips to a1
    lea     $dff000,a1
    
    ; Disable operating system interrupts
    move.w  #$7fff,$9a(a1)      ; INTENA

    ; Start the Copper List
    lea     copper_list(pc),a0
    move.l  a0,$80(a1)          ; COP1LC

frameloop:

    bra.s   frameloop

copper_list:
    dc.w    $08e,$2c81          ; DIWSTRT
    dc.w    $090,$2cc1          ; DIWSTOP
    dc.w    $092,$0038          ; DDFSTRT
    dc.w    $094,$00d0          ; DDFSTOP
    dc.w    $180,$0f00          ; COLOR00
    dc.w    $182,$00f0          ; COLOR01
    dc.w    $184,$000f          ; COLOR02
    dc.w    $186,$0fff          ; COLOR03
	dc.w    $100,$2100          ; BPLCON0 (2 planes)
    dc.w    $096,$8201          ; DMACON
    dc.w    $0e0,$0004          ; BPL1PTH
    dc.w    $0e2,$0000           
    dc.w    $0e4,$0004          ; BPL2PTH
    dc.w    $0e6,$2800           
    dc.w    $ffff,$fffe         ; End of Copper list